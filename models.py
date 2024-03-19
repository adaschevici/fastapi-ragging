from pydantic import BaseModel

class Message(BaseModel):
    msg: str

class CreateIndexPayload(BaseModel):
    urls: list[str]

class SearchPayload(BaseModel):
    query: str
