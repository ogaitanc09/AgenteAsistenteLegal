import os
from typing import Any, Dict

from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from api.config_llm import groq_llm, create_retrieval_chain
from api.memory import with_memory
from api.rag_loader import load_rag_for_topic
from api.prompt_templates import legal_chat_prompt, render_chat_history


def build_legal_agent(topic_name: str):
    """
    Agente legal ReAct compatible con LangChain 1.0.x.
    - Usa RAG (retriever -> chain)
    - Usa memoria global (with_memory)
    - Detecta cuándo llamar a la herramienta 'buscar_documentos_legales'
    """

    print(f" Cargando vectorstore para el tema: {topic_name}")

    # 1) Cargar retriever desde rag_loader
    retriever = load_rag_for_topic(topic_name)

    # 2) Crear chain RAG (acepta directamente un retriever)
    rag_chain = create_retrieval_chain(retriever)

  
    # 3) Wrap del RAG como herramienta

    def tool_buscar_documentos_legales(q):
        """Tool: busca en el vectorstore usando RAG."""
        if isinstance(q, dict):
            q = q.get("input", "") or q.get("query", "")
        return rag_chain.invoke(q)

    tools = {
        "buscar_documentos_legales": Tool.from_function(
            func=tool_buscar_documentos_legales,
            name="buscar_documentos_legales",
            description="Busca información legal en el vectorstore seleccionado.",
        )
    }

    #  Se deja el prompt original TAL CUAL 
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente legal experto. Usa SOLO el contexto provisto por la herramienta cuando la invoques."),
        ("human", "{input}")
    ])

    # 5) Heurística simple para decidir si usar la herramienta
    def should_use_tool(text: str) -> bool:
        t = text.lower()
        trigger_words = ["ley", "norma", "artículo", "buscar", "contrato", "empleador", "empleado"]
        return any(w in t for w in trigger_words)

   
    # 6) EJECUTOR DEL AGENTE (ReAct manual)

    def agent_executor(inputs: Dict[str, Any]):
        """
        inputs example: {"input": "¿Qué dice la ley X?", "chat_history": [...]}
        """
        user_text = inputs.get("input", "")
        if not user_text:
            return "No recibí texto de entrada."


        if should_use_tool(user_text):
            print(" Decision: invocar herramienta 'buscar_documentos_legales'")

            result = tools["buscar_documentos_legales"].invoke(user_text)
            return f" Resultado encontrado:\n{result}"

        else:
            print(" Decision: responder directamente con LLM usando memoria")

            # Recuperamos historial inyectado automáticamente por with_memory()
            chat_history = inputs.get("chat_history", [])
            chat_history_text = render_chat_history(chat_history)

            # Renderizamos el prompt completo con historial + pregunta
            rendered_prompt = legal_chat_prompt.format(
                input=user_text,
                chat_history=chat_history_text
            )

            # Llamada al modelo
            llm_resp = groq_llm.invoke(rendered_prompt)
            return llm_resp.content if hasattr(llm_resp, "content") else str(llm_resp)

 
    # 7) Construcción del chain

    chain = (
        RunnablePassthrough.assign(input=lambda d: d.get("input"))
        | agent_executor
        | StrOutputParser()
    )

 
    # 8) Añadir memoria global

    chain_with_memory = with_memory(chain)

    print(" Agente legal ReAct listo con memoria + RAG + herramientas.")
    return chain_with_memory
