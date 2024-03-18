from langchain_community.embeddings import HuggingFaceEmbeddings

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
text = "This is a test document."

res = hf.embed_query(text)

if __name__ == "__main__":
    print(len(res))
