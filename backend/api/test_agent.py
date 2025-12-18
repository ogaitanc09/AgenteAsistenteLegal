# backend/api/test_agent.py

import sys
import os

# Asegurar import desde la raíz del proyecto
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_PATH)

from backend.api.react_agent import build_legal_agent

if __name__ == "__main__":
    print(" INICIANDO PRUEBA DEL AGENTE LEGAL RAG + REACT + MEMORIA\n")

    topic = "codigo_trabajo_vs"
    print(f" Cargando base vectorial seleccionada por usuario: {topic}\n")

    agent = build_legal_agent(topic)

    # Se puede usar cualquier string como session_id
    config = {"configurable": {"session_id": "test123"}}


    # Pregunta 1 (usa RAG)

    p1 = "¿Cuáles son las obligaciones principales del empleador según la ley?"
    print(" PREGUNTA 1:\n", p1)

    r1 = agent.invoke({"input": p1}, config)

    print("\n RESPUESTA 1:\n", r1)

 
    # Pregunta 2 (usa memoria sobre lo anterior)

    p2 = "¿Puedes resumir lo que acabas de explicar?"
    print("\n PREGUNTA 2 (usa memoria):\n", p2)

    r2 = agent.invoke({"input": p2}, config)

    print("\n RESPUESTA 2:\n", r2)


    # Pregunta 3 (usa memoria)

    p3 = "¿Qué obligaciones mencionaste anteriormente? Dámelas nuevamente."
    print("\n PREGUNTA 3 (usa memoria):\n", p3)

    r3 = agent.invoke({"input": p3}, config)

    print("\n RESPUESTA 3:\n", r3)

