from retrieval.vector_store import VectorStore

class SearchEngine:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def query(self, text: str, top_k: int = 5):
        # Placeholder for similarity search
        vectors = self.vector_store.get_vectors()
        results = []
        for v in vectors:
            if text.lower() in v.get("metadata", {}).get("text", "").lower():
                results.append(v)
        return results[:top_k]

if __name__ == "__main__":
    from retrieval.vector_store import VectorStore
    store = VectorStore()
    store.add_vector([0.1, 0.2, 0.3], {"text": "Hello world"})
    se = SearchEngine(store)
    print(se.query("hello"))
