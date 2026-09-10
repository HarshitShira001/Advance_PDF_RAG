# PDF RAG

A containerized FastAPI-based Retrieval-Augmented Generation (RAG) application for uploading PDFs and asking context-based questions.

## Features

- PDF storage using AWS S3
- Text extraction and chunking using LangChain
- Semantic embeddings using Jina Embeddings
- Vector storage and similarity search using Qdrant
- Asynchronous PDF processing using RQ + Valkey
- File metadata and results stored in MongoDB
- AI responses generated using `openai/gpt-oss-120b`
- Docker & Docker Compose for containerized deployment
- Nginx for reverse proxy
- Designed for AWS EC2 cloud deployment

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI, Python |
| LLM | `openai/gpt-oss-120b` |
| Embeddings | Jina Embeddings |
| Vector DB | Qdrant |
| Database | MongoDB |
| Task Queue | RQ + Valkey |
| Cloud Storage | AWS S3 |
| Reverse Proxy | Nginx |
| Containerization | Docker, Docker Compose |
| Cloud | AWS EC2 |

## Setup

### Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=<your_groq_api_key>
JINA_API_KEY=<your_jina_api_key>
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_REGION=<your_aws_region>
S3_BUCKET_NAME=<your_bucket_name>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run with Docker

```bash
docker compose up -d
```

### Run the RQ Worker

```bash
sh rq.sh
```

### Run FastAPI

```bash
sh run.sh
```

## API

### Qdrant Dashboard

```text
http://localhost:6333/dashboard
```

## RAG Pipeline

```text
PDF
 ↓
AWS S3
 ↓
RQ + Valkey
 ↓
PDF Processing
 ↓
Jina Embeddings
 ↓
Qdrant
 ↓
Similarity Search
 ↓
openai/gpt-oss-120b
 ↓
AI Answer
```

## Deployment

The application can be deployed on AWS EC2 using Docker Compose, with AWS S3 providing scalable object storage, Nginx acting as a reverse proxy, and Docker containers managing the application services.
