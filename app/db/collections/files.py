from pydantic import BaseModel, Field
from typing import Optional
from pymongo.collection import Collection

from ..db import database


class FileSchema(BaseModel):
    name: str = Field(..., description="Name of the file")
    status: str = Field(..., description="Status of the file")
    result: Optional[str] = Field(None, description="The result from AI")


COLLECTION_NAME = "files"

files_collection: Collection = database[COLLECTION_NAME]