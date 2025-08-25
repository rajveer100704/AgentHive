import numpy as np

class VectorStore:
    def __init__(self):
        self.store = []

    def add_vector(self, vector: list, metadata: dict = None):
        self.store.append({"vector": np.array(vector), "metadata": metadata or {}})

    def get_vectors(self):
        return self.store

    def similarity_search(self, query_vector: list, top_k: int = 5):
        """Returns top-k closest vectors"""
        if not self.store:
            return []
        query_vec = np.array(query_vector)
        distances = []
        for item in self.store:
            dist = np.linalg.norm(query_vec - item["vector"])
            distances.append((dist, item))
        distances.sort(key=lambda x: x[0])
        return [item for _, item in distances[:top_k]]

