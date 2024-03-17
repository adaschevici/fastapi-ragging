from fastapi import APIRouter, Depends
from models import Message
from starlette.requests import Request
from bootstrap import get_logger

router = APIRouter()



@router.get("/")
async def root(logger = Depends(get_logger)):
    logger.info("Hello World")
    return {"message": "Hello World"}

@router.post("/search")
async def search(query: Message):
    return {"message": query}

@router.post("/create-index")
async def create_index():
    return {"message": "Index created"}
