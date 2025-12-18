# backend/api/create_vectorstore.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# CONFIGURACIÓN GENERAL

RAGS_PATH = "backend/rags"
VECTORSTORES_PATH = "backend/vectorstores"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

FOLDER_TO_PROCESS = "reglamentos"   # NombreCarpeta

# Crear carpeta donde van todas las bases vectoriales
os.makedirs(VECTORSTORES_PATH, exist_ok=True)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# PROCESAR UNA SOLA CARPETA (1 PDF)

def process_folder(folder_name):
    folder_path = os.path.join(RAGS_PATH, folder_name)

    if not os.path.isdir(folder_path):
        print(f"La carpeta '{folder_name}' no existe en backend/rags/")
        return

    print(f"\n Procesando carpeta: {folder_name}")

    # Buscar PDF dentro de la carpeta
    pdf_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print(f"No hay PDFs dentro de {folder_path}")
        return

    # Procesamos el PRIMER PDF encontrado
    pdf_path = os.path.join(folder_path, pdf_files[0])
    print(f"PDF detectado: {pdf_path}")

    # 1. Cargar PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"   Total páginas: {len(documents)}")

    # 2. Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    splits = splitter.split_documents(documents)
    print(f"   Chunks generados: {len(splits)}")

    # 3. Crear carpeta única para esta base vectorial
    persist_path = os.path.join(VECTORSTORES_PATH, f"{folder_name}_vs")
    os.makedirs(persist_path, exist_ok=True)

    print(f"   Creando Vectorstore en: {persist_path}")

    # 4. Crear vectorstore
    texts = [doc.page_content for doc in splits]
    metadatas = [doc.metadata for doc in splits]

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=persist_path
    )

    vectorstore.persist()

    print("\n✔ Vectorstore creado exitosamente.")
    print(f"✔ Total chunks indexados: {vectorstore._collection.count()}")
    print(f" Ubicación: {persist_path}\n")


# -------------------------------------
# EJECUCIÓN AUTOMÁTICA (SIN CONSOLA)
# -------------------------------------

if __name__ == "__main__":
    process_folder(FOLDER_TO_PROCESS)
