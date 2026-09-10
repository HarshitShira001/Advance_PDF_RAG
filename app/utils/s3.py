"""import os
import aiofiles


async def save_to_disk(file: bytes, path: str) -> bool:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    async with aiofiles.open(path, "wb") as out_file:
        await out_file.write(file)

    return True"""
import boto3

S3_BUCKET = "advancerag"
AWS_REGION = "ap-south-1"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


def upload_to_s3(file: bytes, filename: str) -> bool:
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=file,
        ContentType="application/pdf",
    )

    return True


def get_from_s3(filename: str) -> bytes:
    response = s3.get_object(
        Bucket=S3_BUCKET,
        Key=filename
    )

    return response["Body"].read()

def get_s3_url(filename: str) -> str:
    return (
        f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/"
        f"{filename}"
    )
