from langchain_community.embeddings import HuggingFaceEmbeddings


def create_embeddings(text: str):
    model_name = "jinaai/jina-embeddings-v2-small-en"
    model_kwargs = {"device": "mps", "trust_remote_code": True}
    encode_kwargs = {
        "normalize_embeddings": False,
    }
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    res = hf.embed_query(text)
    return res

if __name__ == "__main__":
    text = "I love to code"
    res = create_embeddings(text)
    print(len(res))
