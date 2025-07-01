# services/db_service.py
from typing import Tuple

from database.engine import SessionLocal
from database.models.sprite import Sprite
from database.models.tag import Tag
from database.models.tag_type import TagType

from database.repositories.sprite_repository import SpriteRepository
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