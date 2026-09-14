# PDF RAG

A containerized **Retrieval-Augmented Generation (RAG)** application for uploading PDFs and generating context-aware answers using semantic search and LLMs.

## Features

* PDF storage using **AWS S3**
* Text extraction and chunking using **LangChain**
* Semantic **embeddings** for document representation
* Vector storage and similarity search using **Qdrant**
* Asynchronous document processing using **RQ + Valkey**
* Metadata and processing status stored in **MongoDB**
* AI responses generated using `openai/gpt-oss-120b`
* Containerized deployment using **Docker & Docker Compose**
* **Nginx** reverse proxy for secure traffic routing
* **HTTPS/SSL certificate** for encrypted communication
* **SSH** for secure remote server administration
* **AWS IAM** for access and permission management
* Designed for **AWS EC2 cloud deployment**

## Tech Stack

| Component         | Technology             |
| ----------------- | ---------------------- |
| Backend           | FastAPI, Python        |
| LLM               | `openai/gpt-oss-120b`  |
| Embeddings        | Embedding Model        |
| Vector DB         | Qdrant                 |
| Database          | MongoDB                |
| Task Queue        | RQ + Valkey            |
| Storage           | AWS S3                 |
| Access Management | AWS IAM                |
| Reverse Proxy     | Nginx                  |
| Security          | HTTPS/SSL, SSH         |
| Containerization  | Docker, Docker Compose |
| Cloud             | AWS EC2                |

## Setup

### Environment Variables

Create a `.env` file:

```env
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

### Run RQ Worker

```bash
sh rq.sh
```

### Run FastAPI

```bash
sh run.sh
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
Embeddings
 ↓
Qdrant
 ↓
Semantic Search
 ↓
openai/gpt-oss-120b
 ↓
AI Answer
```

## API

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

Qdrant Dashboard:

```text
http://localhost:6333/dashboard
```

## Deployment & Security

The application is designed for **AWS EC2** deployment using Docker Compose.

**Nginx** acts as a reverse proxy and routes external traffic to internal application services.

**HTTPS/SSL certificates** provide encrypted communication between clients and the server.

**SSH** is used for secure remote server administration and deployment.

**AWS IAM** manages access permissions for AWS resources following the principle of least privilege.

```text
Client
  ↓
HTTPS / SSL
  ↓
Nginx
  ↓
FastAPI / Streamlit
  ↓
Docker Services
  ↓
AWS S3 / MongoDB / Qdrant / RQ
```
demo video
https://drive.google.com/file/d/1Hb5Xu1PLU9hUcmTJQdFIrinyFvICuXqU/view
