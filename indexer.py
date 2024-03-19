import requests
import math
from embedding_tools import create_embeddings
from bs4 import BeautifulSoup
from qdrant_client import models
from uuid import uuid4
from app_logging import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient


class Indexer:
    MODEL_CHUNK_SIZE = 8192
    EMBEDDING_SIZE = 512

    def __init__(self, qdrant_client, qdrant_collection_name):
        self.qdrant_client = qdrant_client
        self.qdrant_collection_name = qdrant_collection_name
        self.qdrant_client.recreate_collection(
            collection_name=self.qdrant_collection_name,
            vectors_config=models.VectorParams(size=self.EMBEDDING_SIZE, distance=models.Distance.COSINE),
        )
        

    def get_html_body_content(self, url) -> str:
        # This method is not implemented in this snippet
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        body = soup.body
        inner_text = body.get_text()
        return inner_text

    def index_url_document(self, urls: list[str]):
        for url in urls:
            self.index_document(url)

    def index_document(self, url: str):
        try:
            content = self.get_html_body_content(url)
            self.add_to_vector_db(content, url)
        except Exception as e:
            logger.error(f"Failed to index document {url} with error: {e}")
            

    def add_to_vector_db(self, content: str, url: str):
        splitter = RecursiveCharacterTextSplitter(
            max_chunk_size=self.MODEL_CHUNK_SIZE,
            chunk_overlap=math.floor(self.MODEL_CHUNK_SIZE * 0.1),
        )
        chunks = splitter.create_documents([content])
        for chunk in chunks:
            embedding = create_embeddings(chunk.page_content)
            self.insert_embeddings(embedding, chunk.page_content, url)

    def insert_embeddings(self, embedding: list[float], content: str, url: str):
        # TODO: this probaly needs to be a batch operation
        self.qdrant_client.upsert(
            collection_name=self.qdrant_collection_name,
            ids=[uuid4().hex],
            vectors=[embedding],
            external_ids=[url],
            payloads=[{"content": content}],
        ) 


if __name__ == "__main__":
    qdrant_client = QdrantClient("localhost", port=6333)
    indexer = Indexer(qdrant_client, "test_collection")
    indexer.index_document("https://fastapi.tiangolo.com/deployment/manually/")
    print(indexer)
