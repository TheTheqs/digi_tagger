# database/repositories/embedding_repository.py

import pickle
from sqlalchemy.orm import Session
from database.models.embedding import Embedding

class EmbeddingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_many(self, embeddings: list[Embedding]):
        self.session.add_all(embeddings)

    def exists_by_sprite_and_source(self, sprite_id: int, source: str) -> bool:
        return self.session.query(Embedding).filter_by(sprite_id=sprite_id, source=source).first() is not None

    def get_all_by_source(self, source: str) -> list[tuple[int, object]]:
        results = (
            self.session.query(Embedding.sprite_id, Embedding.vector)
            .filter_by(source=source)
            .all()
        )
        # Desserializa os vetores antes de retornar
        return [(sprite_id, pickle.loads(vector)) for sprite_id, vector in results]
