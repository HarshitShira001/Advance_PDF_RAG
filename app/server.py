from fastapi import FastAPI, UploadFile, Path, Form
from .db.collections.files import files_collection, FileSchema
from .queue.q import q
from .queue.workers import process_file
from .utils.s3 import upload_to_s3, get_s3_url
from bson import ObjectId


app = FastAPI()


@app.get("/")
def hello():
    return {"status": "healthy"}


@app.get("/{id}")
async def get_file_by_id(
    id: str = Path(..., description="ID of the file")
):
    db_file = files_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if not db_file:
        return {"error": "File not found"}

    return {
        "_id": str(db_file["_id"]),
        "name": db_file["name"],
        "status": db_file["status"],
        "result": db_file.get("result"),
    }


@app.post("/upload")
async def upload_file(
    file: UploadFile,
    question: str = Form(..., description="User's question")
):

    # 1. Create MongoDB record
    db_file = files_collection.insert_one(
        FileSchema(
            name=file.filename,
            status="saving"
        )
    )

    file_id = str(db_file.inserted_id)

    # 2. Read uploaded file
    file_data = await file.read()

    # 3. Create S3 key
    s3_key = f"uploads/{file_id}/{file.filename}"

    # 4. Upload to S3
    try:
        upload_to_s3(
            file=file_data,
            filename=s3_key
        )

    except Exception as e:

        files_collection.update_one(
            {"_id": db_file.inserted_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )

        return {
            "error": "Failed to upload file"
        }

    # 5. Update MongoDB
    files_collection.update_one(
        {"_id": db_file.inserted_id},
        {
            "$set": {
                "status": "queued",
                "s3_key": s3_key
            }
        }
    )

    # 6. Add job to RQ
    q.enqueue(
        process_file,
        file_id,
        s3_key,
        question
    )

    # 7. Return immediately
    return {
        "file_id": file_id,
        "status": "queued",
        "s3_key": s3_key,
        "pdf_url": get_s3_url(s3_key)
    }