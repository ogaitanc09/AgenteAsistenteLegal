# backend/api/memory.py

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Una sola instancia de ChatMessageHistory para toda la app.
_global_history = ChatMessageHistory()

def _get_global_history(_config = None):
    # Ignoramos cualquier config y devolvemos la misma memoria global.
    return _global_history

def with_memory(chain):
    """
    Envuelve cualquier chain con memoria conversacional global.
    Configuración clave: `configurable_fields=None` evita que RunnableWithMessageHistory
    exija que el usuario pase session_id en cada invoke().
    """
    return RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=lambda config: _get_global_history(config),
        input_messages_key="input",
        history_messages_key="chat_history",
        configurable_fields=None,  # <-- evita requerir session_id
    )
