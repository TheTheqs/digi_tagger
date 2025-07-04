import numpy as np
from database.db_service import DBService
from services.strategies.embeddings.clip_strategy import CLIPEmbeddingStrategy

def deserialize_test() -> tuple[bool, str]:
    subject = DBService().get_sprite_by_id(12)
    if subject is not None:
        print(f"[DEBUG] Tipo de subject.vector: {type(subject.vector)}")
        print(f"[DEBUG] Início dos bytes: {subject.vector[:10]}")
        result = CLIPEmbeddingStrategy().deserialize_embedding(subject.vector)
        return isinstance(result, np.ndarray), "deserialize_test"
    print("[TEST] deserialize_test: Nenhum sprite com ID 0 encontrado.")
    return False, "deserialize_test"
