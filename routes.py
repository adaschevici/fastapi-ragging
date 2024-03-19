from fastapi import APIRouter, Depends
from models import Message, CreateIndexPayload, SearchPayload
from bootstrap import get_logger, get_qdrant_client

router = APIRouter()


@router.get("/")
async def root(logger=Depends(get_logger)):
    logger.info("Hello World")
    logger.debug("Debugging")
    return {"message": "Hello World"}


@router.post("/search")
async def search(
    query: SearchPayload, qdrant_client=Depends(get_qdrant_client), logger=Depends(get_logger)
):
    return {"message": query}


@router.post("/create-index")
async def create_index(
    urls: CreateIndexPayload, qdrant_client=Depends(get_qdrant_client), logger=Depends(get_logger)
):
    return {"message": "Index created"}
