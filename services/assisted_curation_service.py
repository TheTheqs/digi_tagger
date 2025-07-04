from typing import List
from torch import cosine_similarity
import torch
from database.dtos import SpriteResponseDTO
from services.strategies.embeddings.base import EmbeddingStrategy

class AssistedCurationService:
    def __init__(self, strategy: EmbeddingStrategy):
        self.strategy = strategy

    def get_top_k_similar(
            self,
            tag_description: str,
            sprites: List[SpriteResponseDTO],
            top_k: int = 10
    ) -> List[SpriteResponseDTO]:
        tag_embedding = self.strategy.get_text_embedding(tag_description).reshape(1, -1)
        tag_tensor = torch.from_numpy(tag_embedding)

        ranked_results = []

        for sprite in sprites:
            try:
                embedding = self.strategy.deserialize_embedding(sprite.vector).reshape(1, -1)
                image_tensor = torch.from_numpy(embedding)

                # Cálculo correto da similaridade com extração do valor escalar
                similarity_score = cosine_similarity(tag_tensor, image_tensor).item()

                ranked_results.append((similarity_score, sprite))

            except Exception as e:
                print(f"[WARN] Erro ao processar sprite {sprite.path}: {e}")

        # Ordena os resultados do maior para o menor
        ranked_results.sort(key=lambda x: x[0], reverse=True)

        # Retorna apenas os sprites no top K
        return [sprite for _, sprite in ranked_results[:top_k]]
