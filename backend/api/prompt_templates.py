# backend/api/prompt_templates.py

from typing import List, Any
from langchain_core.prompts import ChatPromptTemplate

assistant_system_prompt = """
Eres un asistente jurídico avanzado diseñado para ofrecer respuestas claras, precisas y profesionales.
Debes mantener siempre un tono humano, experto y contextualizado al derecho colombiano.

REGLAS DE COMPORTAMIENTO:

1. Usa como primera fuente el contexto recuperado por el sistema.
2. Si el contexto es insuficiente, ambiguo o no aborda directamente la pregunta:
   - Completa la respuesta usando tu razonamiento jurídico general.
   - Nunca menciones la ausencia de información.
   - Nunca menciones “documentos”, “bases de datos”, “contexto recuperado” ni nada técnico.
3. Cuando cites normas o artículos:
   - Solo hazlo si están explícitamente incluidos en el contexto.
   - Si no hay normas disponibles, explica los conceptos jurídicos sin citarlas.
4. Responde SIEMPRE a la pregunta del usuario.
5. Mantén un lenguaje natural, profesional y claro, evitando sonar mecánico o robótico.
6. Nunca des excusas técnicas ni describas procesos internos del sistema.
"""

# Prompt que incluye el historial ya formateado como texto
legal_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", assistant_system_prompt),
    # Chat history será un string construido antes de llamar a .format()
    ("human", "{chat_history}\n\nPregunta: {input}")
])


def render_chat_history(history: List[Any]) -> str:
    """
    Convierte la lista `chat_history` que inyecta RunnableWithMessageHistory
    a un string legible para el LLM.

    `history` puede ser:
    - una lista de dicts con {'role': 'user'|'assistant', 'content': '...'}
    - una lista de tuples, o ya un string (en cuyo caso se devuelve tal cual).
    """
    if history is None:
        return ""

    # Si ya es un string, devuélvelo
    if isinstance(history, str):
        return history

    out_lines = []
    for msg in history:
        # Manejar dicts: {'role': ..., 'content': ...}
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            out_lines.append(f"{role.capitalize()}: {content}")
        # Manejar tuplas/listas: (role, content)
        elif isinstance(msg, (list, tuple)) and len(msg) >= 2:
            role, content = msg[0], msg[1]
            out_lines.append(f"{str(role).capitalize()}: {content}")
        # Fallback: str()
        else:
            out_lines.append(str(msg))

    # Limita longitud si es demasiado largo (opcional)
    joined = "\n".join(out_lines)
    return joined
