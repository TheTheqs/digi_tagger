# services/strategies/clustering/base.py

from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, List

class ClusteringStrategy(ABC):
    @abstractmethod
    def cluster(self, embeddings: np.ndarray) -> Dict[int, List[int]]:
        """
        Agrupa embeddings em clusters.

        :param embeddings: Embeddings (N, D)
        :return: Dicionário de clusters, onde chave é cluster_id e valores são índices dos elementos.
        """
        pass
