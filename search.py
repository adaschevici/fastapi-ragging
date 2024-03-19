from embedding_tools import create_embeddings
from bootstrap import get_logger

logger = get_logger()

class Search:

    def __init__(self, qdrant_client, qdrant_collection_name):
        self.qdrant_client = qdrant_client
        self.qdrant_collection_name = qdrant_collection_name

    def query_qdrant(self, embedding, limit=10):
        results = self.qdrant_client.search(
            collection_name=self.qdrant_collection_name,
            query_vector=embedding,
            limit=limit,
        )
        list_of_documents = list(map(lambda match: match.payload.get("content"), results))
        list_of_sources = list(map(lambda match: match.payload.get("url"), results))
        return {
            "documents": list_of_documents,
            "sources": list_of_sources
        }

    def query_llm(self, query: str, context: str):
        embeddings = create_embeddings(query)
        return self.query_qdrant(embeddings)

    def search(self, user_query: str):
        embedding = create_embeddings(user_query)
        results = self.query_qdrant(embedding)
        logger.info(f"Search results: {results}")
        return results
