import os
import json
from app.config import VECTOR_DIM, EMBEDDING_MODEL, MAX_RETRIEVAL_RESULTS
from retrieval.vector_store import VectorStore
from ingestion.preprocess import preprocess_data
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from typing import List, Dict

# Initialize embedding model and OpenAI client
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Vector store for documents
vector_store = VectorStore()

def embed_text(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts."""
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()

def add_documents(documents: List[Dict]):
    """Preprocess, embed, and add documents to vector store."""
    processed = preprocess_data(documents)
    texts = [item["text"] for item in processed]
    embeddings = embed_text(texts)
    for doc, vec in zip(processed, embeddings):
        vector_store.add_vector(vec, metadata=doc.get("meta", {}))

def query_llama3(query: str, top_k: int = MAX_RETRIEVAL_RESULTS):
    """Retrieve top-k relevant documents and generate LLM response."""
    query_embedding = embed_text([query])[0]
    results = vector_store.similarity_search(query_embedding, top_k)

    # Combine retrieved context
    context = "\n".join([r["metadata"].get("text", "") for r in results])

    # Generate response using LLaMA3 / OpenAI API
    prompt = f"Answer the query using the following context:\n{context}\n\nQuery: {query}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful research assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    # Example usage
    docs = [
        {"text": "Natural Language Processing enables machines to understand text.", "meta": {"source": "wiki"}},
        {"text": "Transformers are powerful models for NLP tasks.", "meta": {"source": "blog"}}
    ]
    add_documents(docs)
    query = "Explain NLP transformers"
    answer = query_llama3(query)
    print("LLaMA3 Response:\n", answer)
