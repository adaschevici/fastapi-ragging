from fastapi import FastAPI
from config import get_settings
from qdrant_client import QdrantClient

settings = get_settings()

async def setup_qdrant(app: FastAPI):
    app.state._qdrant_client = QdrantClient(settings.qdrant_host, port=settings.qdrant_port)

async def teardown_qdrant(app: FastAPI):
    app.state._qdrant_client.close()
    del app.state._qdrant_client
