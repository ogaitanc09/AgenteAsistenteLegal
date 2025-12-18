# backend/api/react_agent.py

from typing import Dict, Any, List, Union
import traceback

from langchain_core.tools import Tool
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from api.config_llm import groq_llm, create_retrieval_chain
from api.memory import with_memory
from api.rag_loader import load_rag_for_topic
from api.prompt_templates import legal_chat_prompt, render_chat_history


def _normalize_rag_result(result: Any) -> str:
    """
    Convierte la salida de rag_chain.invoke(...) a texto plano seguro.
    Acepta:
      - str
      - dict con keys habituales: "context", "answer", "texts", "documents"
      - objeto con .content
      - lista -> une elementos
      - cualquier otro -> str(...)
    """
    try:
        if result is None:
            return ""

        # Si ya es string
        if isinstance(result, str):
            return result.strip()

        # Si es lista/tupla -> unir
        if isinstance(result, (list, tuple)):
            return "\n".join([str(x).strip() for x in result if x is not None]).strip()

        # Si es dict-like: buscar keys habituales
        if isinstance(result, dict):
            # Preferir 'context' > 'answer' > 'texts' > 'documents'
            if "context" in result:
                ctx = result.get("context") or []
                if isinstance(ctx, str):
                    return ctx.strip()
                if isinstance(ctx, (list, tuple)):
                    return "\n".join([str(x).strip() for x in ctx if x is not None]).strip()
            if "answer" in result and isinstance(result["answer"], str):
                return result["answer"].strip()
            if "texts" in result:
                t = result.get("texts") or []
                if isinstance(t, str):
                    return t.strip()
                if isinstance(t, (list, tuple)):
                    return "\n".join([str(x).strip() for x in t if x is not None]).strip()
            if "documents" in result:
                docs = result.get("documents") or []
                # documents might be objects - convert to text
                if isinstance(docs, str):
                    return docs.strip()
                if isinstance(docs, (list, tuple)):
                    return "\n".join([str(getattr(d, "page_content", d)).strip() for d in docs if d is not None]).strip()

        # Si tiene .content (objeto LLM-like)
        if hasattr(result, "content"):
            try:
                return str(result.content).strip()
            except Exception:
                pass

        # Fallback: str()
        return str(result).strip()
    except Exception:
        # Nunca lanzar aquí: devolver cadena vacía o el str del traceback para logs
        return ""


def build_legal_agent(topic_name: str):

    print(f" Cargando vectorstore para el tema: {topic_name}")

    # 1) Cargar retriever y crear RAG chain
    retriever = load_rag_for_topic(topic_name)
    rag_chain = create_retrieval_chain(retriever)

 
    # TOOL: Devuelve SOLO el texto del contexto recuperado
    # Maneja robustamente distintos tipos de salida del rag_chain

    def tool_buscar_documentos_legales(q: Union[str, Dict[str, Any]]) -> str:
        try:
            # rag_chain.invoke puede aceptar str o dict dependiendo de su implementación
            raw = rag_chain.invoke(q)
        except Exception as exc:
            # Log interno para debugging; no exponer al usuario
            print("⚠ Error invocando rag_chain:", repr(exc))
            traceback.print_exc()
            return ""

        # Normalizar a texto plano
        context_text = _normalize_rag_result(raw)
        return context_text

    tools = {
        "buscar_documentos_legales": Tool.from_function(
            func=tool_buscar_documentos_legales,
            name="buscar_documentos_legales",
            description="Recupera textos relevantes del tema legal seleccionado."
        )
    }

  
    # EJECUTOR DEL AGENTE (ReAct manual)

    def agent_executor(inputs: Dict[str, Any]) -> str:
        question = inputs.get("input", "")
        if not question:
            return "No recibí ninguna pregunta."

        print(" Ejecutando agente jurídico...")

        # 1) Recuperar documentos relevantes desde RAG (texto plano)
        try:
            rag_context = tools["buscar_documentos_legales"].invoke(question) or ""
        except Exception as exc:
            # Log interno y continuar con contexto vacío (fallback)
            print(" Error en la herramienta de búsqueda:", repr(exc))
            traceback.print_exc()
            rag_context = ""

        # 2) Renderizar historial (seguro)
        history_text = render_chat_history(inputs.get("chat_history", []))

        # 3) Construir prompt mediante legal_chat_prompt de forma segura
        try:
            prompt_value = legal_chat_prompt.format(chat_history=history_text, input=question)
        except Exception as e:
            # Si el template falla, hacemos un fallback seguro
            print(" Warning: legal_chat_prompt.format falló:", repr(e))
            traceback.print_exc()
            prompt_value = None

        # 4) Conservar una lista de mensajes para invocar LLM
        messages: List[Dict[str, str]] = []
        if prompt_value is not None and hasattr(prompt_value, "to_messages"):
            # PromptValue -> mensajes
            try:
                messages = prompt_value.to_messages()
            except Exception as e:
                print(" Warning: prompt_value.to_messages falló:", repr(e))
                traceback.print_exc()
                messages = []
        elif isinstance(prompt_value, str):
            messages = [{"role": "user", "content": prompt_value}]
        else:
            # Fallback base
            messages = [
                {"role": "system", "content": "Eres AssistLeg, un asistente jurídico experto."},
                {"role": "user", "content": (history_text + "\n\n" + question).strip()}
            ]

        # 5) Inyectar el contexto recuperado (si existe) como SYSTEM message
        #    Nota: no debe contener texto tipo "documentos" visible al usuario;
        #    aquí lo inyectamos únicamente como apoyo interno.
        if rag_context:
            messages.append({
                "role": "system",
                "content": rag_context
            })

        # 6) Llamada al LLM (capturar excepciones)
        try:
            response = groq_llm.invoke(messages)
        except Exception as exc:
            print(" Error invocando groq_llm:", repr(exc))
            traceback.print_exc()
            # Mensaje amigable al usuario (sin detalles técnicos)
            return "Lo siento, ocurrió un error al procesar la consulta. Intenta de nuevo en unos segundos."

        # 7) Extraer texto de la respuesta LLM
        try:
            if hasattr(response, "content"):
                return response.content
            return str(response)
        except Exception:
            # Fallback
            return str(response)


    # Construcción final del Chain (con memoria)

    chain = (
        RunnablePassthrough.assign(input=lambda d: d.get("input"))
        | agent_executor
        | StrOutputParser()
    )

    chain_with_memory = with_memory(chain)

    print(" Agente legal ReAct optimizado y listo.")
    return chain_with_memory
