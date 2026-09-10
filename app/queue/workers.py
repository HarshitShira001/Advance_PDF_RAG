
import os
from ..db.collections.files import files_collection
from bson import ObjectId
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import JinaEmbeddings
from langchain_qdrant import QdrantVectorStore

from groq import Groq
from ..utils.s3 import get_from_s3

load_dotenv()
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def process_file(id: str, file_path: str, question: str):

    # Step 0: Mark as processing
    files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "processing"}}
    )

    # Step 1: Load and split the PDF

    filename = os.path.basename(file_path)

    file_data = get_from_s3(file_path)

    with open(filename, "wb") as f:
        f.write(file_data)

    loader = PyPDFLoader(filename)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    split_docs = text_splitter.split_documents(docs)

    # Step 2: Create Jina embeddings
    embedder = JinaEmbeddings(
        jina_api_key=os.getenv("JINA_API_KEY"),
        model_name="jina-embeddings-v3"
    )

    # Store embeddings in Qdrant
    vector_store = QdrantVectorStore.from_documents(
        documents=split_docs,
        url="http://qdrant:6333",
        collection_name=f"pdf_rag_{id}",
        embedding=embedder
    )

    # Step 3: Retrieve relevant chunks
    relevant_chunks = vector_store.similarity_search(
        query=question,
        k=5
    )

    # Create context
    context = "\n\n".join(
        doc.page_content
        for doc in relevant_chunks
    )

    # Step 4: Create prompt for Qwen
    SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the context provided below.

If the answer is not available in the context,
say that you could not find the answer in the document.

Context:
{context}
"""

    # Step 5: Generate answer using Ollama + Qwen 2.5
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    output_text = response.choices[0].message.content

    # Step 6: Update DB with result
    files_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": "processed",
                "result": output_text
            }
        }
    )
    os.remove(filename)

    return output_text