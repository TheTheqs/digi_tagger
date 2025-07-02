# services/strategies/clustering/topk_similarity_clustering.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List
from services.strategies.clustering.base import ClusteringStrategy


class TopKSimilarityClusteringStrategy(ClusteringStrategy):
    def __init__(self, top_k: int = 6, max_suggestions: int = 10):
        self.top_k = top_k
        self.max_suggestions = max_suggestions

    def cluster(self, embeddings: np.ndarray) -> Dict[int, List[int]]:
        similarity = cosine_similarity(embeddings)
        suggestions = {}

        count = 0
        for i in range(len(embeddings)):
            sim_scores = similarity[i]
            indices = np.argsort(sim_scores)[::-1][1:self.top_k + 1]
            cluster = [i] + list(indices)

            suggestions[count] = cluster
            count += 1

            if count >= self.max_suggestions:
                break

        return suggestions
