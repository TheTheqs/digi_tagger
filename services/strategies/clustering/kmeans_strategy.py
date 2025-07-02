# services/strategies/clustering/kmeans_strategy.py

import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List
from services.strategies.clustering.base import ClusteringStrategy

class KMeansClusteringStrategy(ClusteringStrategy):
    def __init__(self, n_clusters: int = 10, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state

    def cluster(self, embeddings: np.ndarray) -> Dict[int, List[int]]:
        model = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)
        labels = model.fit_predict(embeddings)

        clusters: Dict[int, List[int]] = {}
        for idx, label in enumerate(labels):
            clusters.setdefault(label, []).append(idx)

        return clusters
