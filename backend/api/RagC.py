# backend/api/rag_loader.py

import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Ruta correcta: subir un nivel (backend/api → backend) y luego vectorstores/
VECTORSTORES_PATH = Path(__file__).resolve().parents[1] / "vectorstores"

def load_rag_for_topic(topic_name: str):
    """
    Carga un vectorstore ya generado en /backend/vectorstores/<topic>_vs
    y devuelve un retriever listo para usar en el agente.

    Ejemplo:
        retriever = load_rag_for_topic("codigo_trabajo_vs")
    """

    persist_dir = VECTORSTORES_PATH / topic_name

    if not persist_dir.exists():
        raise FileNotFoundError(
            f" No se encontró el vectorstore: {persist_dir}\n"
            f"Verifica que exista la carpeta {topic_name} dentro de backend/vectorstores/"
        )

    print(f" Cargando vectorstore desde: {persist_dir}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    print(" Vectorstore cargado y retriever listo.")
    return retriever
