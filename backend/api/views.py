from rest_framework.decorators import api_view
from rest_framework.response import Response

from .react_agent import build_legal_agent   


@api_view(["POST"])
def ask_question(request):
    topic = request.data.get("topic")
    question = request.data.get("question")

    # Crear agente con RAG + memoria + herramientas
    agent = build_legal_agent(topic)

    # Agregar session_id obligatorio
    config = {"configurable": {"session_id": "web_user_1"}}

    # Ejecutar el agente
    answer = agent.invoke({"input": question}, config)

    return Response({"answer": answer})
