# PDF RAG – Retrieval-Augmented Generation from PDFs

A FastAPI-based application that lets users upload PDF files and ask context-based questions. It uses LangChain, OpenAI Embeddings, Qdrant, and Valkey to enable efficient retrieval-augmented generation (RAG).

## Features

- Upload and process PDF documents
- Extract and split text using LangChain
- Generate semantic embeddings with OpenAI
- Store and search document chunks using Qdrant
- Use Valkey (Redis-compatible) for background task queuing
- Ask questions and get relevant answers from uploaded PDFs

## Tech Stack

- Python
- FastAPI
- LangChain
- OpenAI Embeddings
- Qdrant (Vector Database)
- Valkey (Task Queue / In-memory Store)
- Redis Queue (`rq`)
- streamlit

## Setup required:

### Docker Desktop.
### app/queue/.env
    OPENAI_API_KEY=<your_api_key>
### Install requirements.
    pip install -r requirements.txt

## How to run?

### Rebuild and Reload window (For vsCode : ctrl+shift+p and then select the option)
### Run rq worker
    sh rq.sh
### Run server
    sh run.sh
### Run streamlit app
    streamlit run app/streamlit_app.py


## Where to see the results(in browser)?

### For qdrant UI(vector db):
    http://localhost:6333/dashboard
### For main app with UI:
    http://localhost:8501

### Demo Link Video
    https://drive.google.com/file/d/1qMCJsCWgKHLWosQ5uu5EHumKgPTKmIIL/view?usp=sharing
