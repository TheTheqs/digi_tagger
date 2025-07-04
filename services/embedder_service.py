# services/embedder_service.py

from services.strategies.embeddings.base import EmbeddingStrategy

class EmbedderService:
    def __init__(self, embedder_strategy: EmbeddingStrategy):
        self.embedder = embedder_strategy

    def get_serialized_embedding(self, image_path: str) -> bytes:
        return self.embedder.get_serialized_embedding(image_path)