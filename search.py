from embedding_tools import create_embeddings


class Search:

    def __init__(self, qdrant_client, qdrant_collection_name):
        self.qdrant_client = qdrant_client
        self.qdrant_collection_name = qdrant_collection_name

    def query_qdrant(self, embedding, limit=10):
        return self.qdrant_client.search(
            collection_name=self.qdrant_collection_name,
            vectors=[embedding],
            top=limit,
        )
