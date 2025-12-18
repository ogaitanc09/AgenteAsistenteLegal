# AssistLeg – Asistente Legal y Normativo Inteligente

AssistLeg es un asistente legal inteligente diseñado para facilitar la consulta y comprensión de la normativa colombiana mediante lenguaje natural. El sistema integra técnicas de Inteligencia Artificial, específicamente RAG (Retrieval-Augmented Generation) y un Agente ReAct, permitiendo generar respuestas jurídicas claras, fundamentadas y contextualizadas a partir de documentos normativos reales.

Este proyecto fue desarrollado como proyecto académico para la asignatura Sistemas Inteligentes de la Universidad de Pamplona.

## Características principales

- 🔍 Consulta de normativa legal mediante lenguaje natural
- 📚 Recuperación semántica de información (RAG)
- 🧠 Agente ReAct con razonamiento paso a paso
- 🗂️ VectorStores independientes por tema normativo
- 💬 Chat conversacional con historial
- 🧩 Arquitectura modular y escalable
- 🌐 Interfaz web desarrollada en React
- 🔐 Manejo seguro de claves API mediante .env


## Arquitectura general

El sistema está compuesto por los siguientes módulos:

🖥️ Frontend (React)

- Selector de temas normativos
- Interfaz de chat conversacional
- Renderizado de respuestas en formato Markdown
- Comunicación con el backend mediante HTTP (POST)

🧠 Backend (Django + DRF)

- API REST para recibir consultas
- Gestión de tópicos normativos
- Orquestación del agente ReAct
- Manejo de memoria conversacional

📖 Módulo RAG

- Carga de documentos legales (PDF / TXT)
- Fragmentación (chunking) 
- Generación de embeddings
- Recuperación semántica desde vectorstores

🤖 Agente ReAct

- Decide cuándo usar la herramienta RAG
- Integra contexto + historial + pregunta
- Construye prompts jurídicos especializados
- Llama al LLM para generar la respuesta final

🧩 Modelo de Lenguaje (LLM)

- Uso de Groq LLM 
- Generación de respuestas jurídicas fundamentadas

##  Temas normativos soportados

- 📜 Constitución Política de Colombia
- ⚖️ Código Sustantivo del Trabajo
- 🎓 Reglamentos Universitarios

Cada tema cuenta con su vectorstore independiente, lo que garantiza precisión y escalabilidad.

##  Instalación y ejecución
🔹 Requisitos

- Python 3.10+
- Node.js 18+
- npm
- Virtualenv
- Clave API de Groq

##  Ejecutar el Backend (Django)
cd asistente_normativo
venv\Scripts\activate
cd backend
python manage.py runserver


### El backend quedará disponible en:

http://127.0.0.1:8000

##  Ejecutar el Frontend (React)
cd asistente_normativo
cd frontend
npm install
npm start


### El frontend se abrirá en:

http://localhost:3000

##  Variables de entorno

Crear un archivo .env en el backend con:

GROQ_API_KEY=tu_api_key_aqui


###  Nunca subir este archivo al repositorio.
