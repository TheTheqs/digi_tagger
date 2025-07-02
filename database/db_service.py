# services/db_service.py
import pickle
from typing import Tuple

from database.dto.suggestion_response_dto import SuggestionDTO
from database.engine import SessionLocal
from database.models.embedding import Embedding
from database.models.sprite import Sprite
from database.models.suggestion import Suggestion
from database.models.tag import Tag
from database.models.tag_type import TagType
from database.repositories.embedding_repository import EmbeddingRepository

from database.repositories.sprite_repository import SpriteRepository
from database.repositories.suggestion_repository import SuggestionRepository
from database.repositories.tag_repository import TagRepository
from database.repositories.tag_type_repository import TagTypeRepository

class DBService:

    # ------- SPRITE -------
    def create_sprite(self, path: str) -> Sprite:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprite = repo.create_sprite(path)
            session.commit()
            session.refresh(sprite)
            return sprite

    def get_sprite_by_id(self, sprite_id: int) -> Sprite | None:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.get_by_id(sprite_id)

    def get_sprites_by_tag_id(self, tag_id: int) -> list[Sprite]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.get_by_tag_id(tag_id)

    def add_tag_to_sprite(self, sprite_id: int, tag_id: int):
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            repo.add_tag(sprite_id, tag_id)
            session.commit()

    def get_all_unlabeled_sprite_id_paths(self, tag_type_id: int) -> list[tuple[int, str]]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.get_all_unlabeled_by_tag_type(tag_type_id)

    def get_all_sprites(self) -> list[tuple[int, str]]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.get_all_sprite_id_paths()

    def get_sprite_id_by_paths(self, paths: list[str]) -> list[tuple[int, str]]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.get_sprite_id_by_paths(paths)

    def sprite_has_tag_type(self, sprite_id: int, tag_type_id: int) -> bool:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.has_tag_type(sprite_id, tag_type_id)

    # ------- TAG -------
    def create_tag(self, tag_name: str, tag_type_id: int):
        with SessionLocal() as session:
            tag_type_repo = TagTypeRepository(session)
            if not tag_type_repo.get_by_id(tag_type_id):
                raise ValueError(f"TagType com ID {tag_type_id} não existe.")

            tag_repo = TagRepository(session)
            tag = Tag(name=tag_name, tag_type_id=tag_type_id)
            tag_repo.create(tag)
            session.commit()

    def delete_tag(self, tag_id: int):
        with SessionLocal() as session:
            repo = TagRepository(session)
            tag = repo.get_by_id(tag_id)
            if not tag:
                raise ValueError(f"Tag com ID {tag_id} não existe.")
            repo.delete(tag)
            session.commit()

    def get_tags_by_tag_type(self, tag_type_id: int) -> list[Tuple[str, int]]:
        with SessionLocal() as session:
            repo = TagRepository(session)
            return repo.get_tag_id_name_by_tag_type_id(tag_type_id)

    # ------- TAG TYPE -------
    def create_tag_type(self, name: str):
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_type = TagType(name=name)
            repo.create(tag_type)
            session.commit()

    def delete_tag_type(self, tag_type_id: int):
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_type = repo.get_by_id(tag_type_id)
            if not tag_type:
                raise ValueError(f"TagType com ID {tag_type_id} não existe.")
            repo.delete(tag_type)
            session.commit()

    def get_tag_type_by_id(self, tag_type_id: int) -> TagType | None:
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            return repo.get_by_id(tag_type_id)

    def get_all_tag_types(self) -> list[tuple[str, int]]:
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            return repo.get_all_id_name_pairs()

    # ------- EMBEDDING -------
    def create_embeddings(self, embedding_data: list[tuple[int, str, object]]):
        """
        Recebe lista de tuplas (sprite_id, source, np.ndarray)
        """
        with SessionLocal() as session:
            repo = EmbeddingRepository(session)
            embeddings = [
                Embedding(
                    sprite_id=sprite_id,
                    source=source,
                    vector=pickle.dumps(vector)
                )
                for sprite_id, source, vector in embedding_data
            ]
            repo.create_many(embeddings)
            session.commit()

    def embedding_exists(self, sprite_id: int, source: str) -> bool:
        with SessionLocal() as session:
            repo = EmbeddingRepository(session)
            return repo.exists_by_sprite_and_source(sprite_id, source)

    def get_embeddings_by_source(self, source: str) -> list[tuple[int, object]]:
        with SessionLocal() as session:
            repo = EmbeddingRepository(session)
            return repo.get_all_by_source(source)

    # ------- SUGGESTION -------
    def create_suggestion(self, sprite_ids: list[int], description: str = ""):
        with SessionLocal() as session:
            repo = SuggestionRepository(session)
            suggestion = Suggestion(
                description=description,
                verified=False,
                sprites=[session.get(Sprite, sprite_id) for sprite_id in sprite_ids]
            )
            repo.create(suggestion)
            session.commit()

    def get_next_unverified_suggestion(self) -> SuggestionDTO | None:
        with SessionLocal() as session:
            repo = SuggestionRepository(session)
            return repo.get_next_unverified_dto()

    def mark_suggestion_as_verified(self, suggestion_id: int):
        with SessionLocal() as session:
            repo = SuggestionRepository(session)
            repo.mark_verified(suggestion_id)
            session.commit()

    def get_total_suggestions_count(self) -> int:
        with SessionLocal() as session:
            repo = SuggestionRepository(session)
            return repo.count_total_suggestions()