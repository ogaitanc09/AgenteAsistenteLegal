# backend/api/config_llm.py
import os
from dotenv import load_dotenv

# 1. Cargar variables del .env
env_path = os.path.join(os.path.dirname(__file__), "../backend/.env")
print("Buscando .env en:", os.path.abspath(env_path))
load_dotenv(env_path)

groq_api = os.getenv("GROQ_API_KEY")
print(f"Groq Key cargada: {'OK' if groq_api else 'NO'}")

# 2. Imports principales
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 3. Modelo Groq
from langchain_groq import ChatGroq

# 4. Intentar conectar con Groq
try:
    groq_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=groq_api,
        temperature=0.2
    )

    resp = groq_llm.invoke("Hola Groq, ¿me escuchas?")
    print("Groq responde:", resp.content)
    print("Paso 1 completado correctamente: Conexión establecida con Groq.")

except Exception as e:
    print("Error al conectar con Groq:", e)


# 5. Prompt de RAG
prompt = ChatPromptTemplate.from_template("""
Usa SOLO el siguiente contexto para responder:

{context}

Pregunta: {question}
""")


# 🔧 ***ARREGLADO AQUÍ***  
def create_retrieval_chain(retriever):
    """
    Ahora acepta un retriever directamente.
    NO intenta hacer retriever = vectorstore.as_retriever(),
    porque eso daba error.
    """

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | groq_llm
        | StrOutputParser()
    )

    return chain
