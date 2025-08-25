import os
import json
from app.config import VECTOR_DIM, EMBEDDING_MODEL
from retrieval.vector_store import VectorStore
from ingestion.preprocess import preprocess_data
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Initialize embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Vector store for documents
vector_store = VectorStore()

def embed_text(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts."""
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()

def add_documents(documents: List[Dict]):
    """Preprocess, embed, and add documents to the vector store."""
    processed = preprocess_data(documents)
    texts = [item["text"] for item in processed]
    embeddings = embed_text(texts)
    for doc, vec in zip(processed, embeddings):
        vector_store.add_vector(vec, metadata=doc.get("meta", {}))

def query_agent(query: str, top_k: int = 5):
    """Retrieve top-k relevant documents from vector store."""
    query_embedding = embed_text([query])[0]
    results = vector_store.similarity_search(query_embedding, top_k)
    return [{"text": r["metadata"].get("text", ""), "meta": r["metadata"]} for r in results]

if __name__ == "__main__":
    # Example usage
    docs = [
        {"text": "Artificial Intelligence is transforming the world.", "meta": {"source": "wiki"}},
        {"text": "Machine learning models can be deployed in production.", "meta": {"source": "blog"}}
    ]
    add_documents(docs)
    query = "AI applications"
    results = query_agent(query)
    print("Query Results:")
    for r in results:
        print(r)
