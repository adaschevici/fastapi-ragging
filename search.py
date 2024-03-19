from embedding_tools import create_embeddings
from bootstrap import get_logger
from langchain_openai import ChatOpenAI
from config import get_settings
from langchain_core.prompts import ChatPromptTemplate

settings = get_settings()

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
        llm = ChatOpenAI(
            model="gpt-4",
            openai_api_key=settings.openai_api_key.get_secret_value(),
            temperature=0.7,
            max_tokens=300,
        )
        user_content = f"""
            Knowledge Base:
            ---
            {context}
        """
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", """You are an AI coding assistant designed to help users with their programming needs based on the Knowledge Base provided.
        If you dont know the answer, say that you dont know the answer. You will only answer questions related to FastAPI, any other questions, you should say that its out of your responsibilities.
        Only answer questions using data from knowledge base and nothing else."""),
                ("user", user_content),
                ("user", "{input}"),
            ]
        )
        chain = chat_template | llm
        return chain.invoke({"input": query})

    def search(self, user_query: str):
        embedding = create_embeddings(user_query)
        results = self.query_qdrant(embedding)
        knowledge_base = "\n".join(results['documents'])
        response = self.query_llm(user_query, knowledge_base)
        logger.info(f"Search response: {response}")
        return results
