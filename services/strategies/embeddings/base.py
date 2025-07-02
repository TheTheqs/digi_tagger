# services/strategies/embeddings/base.py

from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingStrategy(ABC):
    @abstractmethod
    def embed(self, image_paths: List[str]) -> np.ndarray:
        """
        Gera embeddings para uma lista de caminhos de imagens.

        :param image_paths: Lista de paths para imagens.
        :return: Embeddings em formato (N, D).
        """
        pass
