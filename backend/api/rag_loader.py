# backend/api/rag_loader.py

import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

VECTORSTORES_PATH = Path(__file__).resolve().parents[1] / "vectorstores"

def load_rag_for_topic(topic_name: str):

    persist_dir = VECTORSTORES_PATH / topic_name

    if not persist_dir.exists():
        raise FileNotFoundError(
            f"No se encontró el vectorstore: {persist_dir}"
        )

    print(f" Cargando vectorstore desde: {persist_dir}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings
    )

    # RAG inteligente: MMR → mejor calidad jurídica
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.35}
    )

    print("✔ Vectorstore cargado.")
    return retriever
