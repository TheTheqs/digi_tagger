from abc import ABC, abstractmethod
import numpy as np

class EmbeddingStrategy(ABC):
    @abstractmethod
    def get_serialized_embedding(self, image_path: str) -> bytes:
        pass

    def get_raw_embedding(self, image_path: str) -> np.ndarray:
        raise NotImplementedError("Esta estratégia não implementa retorno cru de embedding.")

    def get_text_embedding(self, text: str) -> np.ndarray:
        raise NotImplementedError("Esta estratégia não implementa embedding textual.")

    def deserialize_embedding(self, data: bytes) -> np.ndarray:
        """
        Desserializa um vetor salvo com np.save contendo 512 float32.
        """
        import io
        import numpy as np

        try:
            with io.BytesIO(data) as buffer:
                embedding = np.load(buffer, allow_pickle=False)

            if not isinstance(embedding, np.ndarray):
                raise TypeError(f"[ERRO] Objeto carregado não é np.ndarray: {type(embedding)}")

            if embedding.dtype != np.float32:
                raise TypeError(f"[ERRO] Embedding com dtype inválido: {embedding.dtype}, esperado float32")

            if embedding.shape != (512,):
                raise ValueError(f"[ERRO] Embedding com shape inválido: {embedding.shape}, esperado (512,)")
            return embedding.reshape(1, -1)

        except Exception as e:
            print(f"[ERRO] Falha ao desserializar embedding: {e}")
            raise