from pydantic import BaseModel

class Message(BaseModel):
    msg: str

class CreateIndexPayload(BaseModel):
    urls: list[str]
    collection_name: str

class SearchPayload(BaseModel):
    query: str
