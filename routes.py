from fastapi import APIRouter, Depends
from models import Message, CreateIndexPayload, SearchPayload
from bootstrap import get_logger, get_qdrant_client
from indexer import Indexer
from search import Search

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
    search = Search(qdrant_client, qdrant_collection_name="web_data")
    results = search.search(query.query)
    return {"message": query}


@router.post("/create-index")
async def create_index(
    payload: CreateIndexPayload, qdrant_client=Depends(get_qdrant_client), logger=Depends(get_logger)
):
    logger.info(f"Creating index for urls: {payload}")
    indexer = Indexer(qdrant_client, qdrant_collection_name="web_data")
    indexer.index_url_documents(payload.urls)
    logger.info(f"Created index for documents from: {payload}")
    return {"message": "Indexed web content successfully"}
