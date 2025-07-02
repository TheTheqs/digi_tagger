# services/strategies/clustering/dbscan_strategy.py

import numpy as np
from sklearn.cluster import DBSCAN
from typing import Dict, List
from services.strategies.clustering.base import ClusteringStrategy

class DBSCANClusteringStrategy(ClusteringStrategy):
    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples

    def cluster(self, embeddings: np.ndarray) -> Dict[int, List[int]]:
        model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        labels = model.fit_predict(embeddings)

        clusters: Dict[int, List[int]] = {}
        for idx, label in enumerate(labels):
            clusters.setdefault(label, []).append(idx)

        return clusters
