# services/suggestion_generator_service.py

from services.strategies.embeddings.base import EmbeddingStrategy
from services.strategies.clustering.base import ClusteringStrategy
from database.dto.suggestion_dto import SuggestionDTO

from typing import List
import numpy as np

class SuggestionGeneratorService:
    def __init__(self, embedding_strategy: EmbeddingStrategy, clustering_strategy: ClusteringStrategy):
        self.embedding_strategy = embedding_strategy
        self.clustering_strategy = clustering_strategy
        self.numpy = np is not None

    def generate_suggestions(self, image_paths: List[str]) -> List[SuggestionDTO]:
        # Etapa 1: gerar embeddings
        embeddings = self.embedding_strategy.embed(image_paths)

        # Etapa 2: clusterizar os embeddings
        clusters = self.clustering_strategy.cluster(embeddings)

        # Etapa 3: montar sugestões
        suggestions = []
        for cluster_id, indices in clusters.items():
            sprite_ids = [i for i in indices]  # indices dos sprites no path list
            suggestion = SuggestionDTO(sprite_indices=sprite_ids, description=f"Grupo {cluster_id}")
            suggestions.append(suggestion)

        return suggestions
