# database/db_service.py

from typing import List
from database.engine import SessionLocal
from database.models.sprite import Sprite
from database.models.tag_type import TagType
from database.repositories.sprite_repository import SpriteRepository
from database.repositories.tag_repository import TagRepository
from database.repositories.tag_type_repository import TagTypeRepository
from database.dtos import (
    SpriteRequestDTO, SpriteResponseDTO, SpriteResumeDTO,
    TagRequestDTO, TagResponseDTO, TagResumeDTO,
    TagTypeRequestDTO, TagTypeResponseDTO
)


class DBService:

    # ------- SPRITE -------
    def create_sprite(self, dto: SpriteRequestDTO) -> SpriteResponseDTO:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprite = repo.create_sprite(dto.path, dto.vector, dto.size)
            session.commit()
            session.refresh(sprite)
            return self._to_sprite_response_dto(sprite)

    def get_sprite_by_id(self, sprite_id: int) -> SpriteResponseDTO | None:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprite = repo.get_by_id(sprite_id)
            return self._to_sprite_response_dto(sprite) if sprite else None

    def get_sprites_by_tag_id(self, tag_id: int) -> List[SpriteResumeDTO]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprites = repo.get_by_tag_id(tag_id)
            return [self._to_sprite_resume_dto(s) for s in sprites]

    def add_tag_to_sprite(self, sprite_id: int, tag_id: int):
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            repo.add_tag(sprite_id, tag_id)
            session.commit()

    def get_all_unlabeled_sprite_id_paths(self, tag_type_id: int) -> List[SpriteResumeDTO]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprites = repo.get_all_unlabeled_by_tag_type(tag_type_id)
            return [self._to_sprite_resume_dto(s) for s in sprites]

    def get_all_sprites(self) -> List[SpriteResumeDTO]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprites = repo.get_all()
            return [self._to_sprite_resume_dto(s) for s in sprites]

    def get_all_sprites_complete(self) -> List[SpriteResponseDTO]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprites = repo.get_all()
            return [self._to_sprite_response_dto(s) for s in sprites]

    def get_sprite_id_by_paths(self, paths: List[str]) -> List[SpriteResumeDTO]:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            sprites = repo.get_sprite_id_by_paths(paths)
            return [self._to_sprite_resume_dto(s) for s in sprites]

    def sprite_has_tag_type(self, sprite_id: int, tag_type_id: int) -> bool:
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            return repo.has_tag_type(sprite_id, tag_type_id)

    def remove_all_tags_from_sprites(self):
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            repo.remove_all_sprite_tags()
            session.commit()

    def remove_tag_from_sprite(self, sprite_id: int, tag_id: int):
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            repo.remove_tag_from_sprite(sprite_id, tag_id)
            session.commit()

    def delete_all_sprites(self):
        with SessionLocal() as session:
            repo = SpriteRepository(session)
            repo.delete_all_sprites()
            session.commit()

    # ------- TAG -------
    def create_tag(self, dto: TagRequestDTO):
        with SessionLocal() as session:
            tag_type_repo = TagTypeRepository(session)
            if not tag_type_repo.get_by_id(dto.tag_type_id):
                raise ValueError(f"TagType com ID {dto.tag_type_id} não existe.")

            tag_repo = TagRepository(session)
            tag_repo.create(dto.tag_type_id, dto.name, dto.description)
            session.commit()

    def delete_tag(self, tag_id: int):
        with SessionLocal() as session:
            repo = TagRepository(session)
            tag = repo.get_by_id(tag_id)
            if not tag:
                raise ValueError(f"Tag com ID {tag_id} não existe.")
            repo.delete(tag)
            session.commit()

    def get_tags_by_tag_type(self, tag_type_id: int) -> List[TagResponseDTO]:
        with SessionLocal() as session:
            repo = TagRepository(session)
            tags = repo.get_by_tag_type_id(tag_type_id)
            return [
                TagResponseDTO(
                    id=tag.id,
                    tag_type_id=tag.tag_type_id,
                    name=tag.name,
                    description=tag.description,
                    sprites=[SpriteResumeDTO(id=s.id, path=s.path, size=s.size) for s in tag.sprites]
                ) for tag in tags
            ]

    def get_all_tags(self) -> list[TagResponseDTO]:
        with SessionLocal() as session:
            repo = TagRepository(session)
            tags = repo.get_all()
            return [
                TagResponseDTO(
                    id=tag.id,
                    tag_type_id=tag.tag_type_id,
                    name=tag.name,
                    description=tag.description,
                    sprites=[SpriteResumeDTO(id=s.id, path=s.path, size=s.size) for s in tag.sprites]
                ) for tag in tags
            ]

    def delete_all_tags(self):
        with SessionLocal() as session:
            repo = TagRepository(session)
            repo.delete_all()
            session.commit()

    # ------- TAG TYPE -------
    def create_tag_type(self, dto: TagTypeRequestDTO) -> TagTypeResponseDTO:
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_type = TagType(name=dto.name)
            repo.create(tag_type)
            session.commit()
            session.refresh(tag_type)
            return TagTypeResponseDTO(id=tag_type.id, name=tag_type.name)

    def delete_tag_type(self, tag_type_id: int):
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_type = repo.get_by_id(tag_type_id)
            if not tag_type:
                raise ValueError(f"TagType com ID {tag_type_id} não existe.")
            repo.delete(tag_type)
            session.commit()

    def get_tag_type_by_id(self, tag_type_id: int) -> TagTypeResponseDTO | None:
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_type = repo.get_by_id(tag_type_id)
            if not tag_type:
                return None
            return TagTypeResponseDTO(id=tag_type.id, name=tag_type.name)

    def get_tag_type_by_name(self, tag_type_name: str) -> TagTypeResponseDTO | None:
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_type = repo.get_by_name(tag_type_name)
            if not tag_type:
                return None
            return TagTypeResponseDTO(id=tag_type.id, name=tag_type.name)

    def get_all_tag_types(self) -> List[TagTypeResponseDTO]:
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            tag_types = repo.get_all()
            return [TagTypeResponseDTO(id=tt.id, name=tt.name) for tt in tag_types]

    def delete_all_tag_types(self):
        with SessionLocal() as session:
            repo = TagTypeRepository(session)
            repo.delete_all()
            session.commit()

    # ------- HELPERS -------

    def _to_sprite_response_dto(self, sprite: Sprite) -> SpriteResponseDTO:
        return SpriteResponseDTO(
            id=sprite.id,
            path=sprite.path,
            vector= sprite.embeddings,
            size=sprite.size,
            tags=[
                TagResumeDTO(id=tag.id, name=tag.name, tag_type_id=tag.tag_type_id)
                for tag in sprite.tags
            ]
        )

    def _to_sprite_resume_dto(self, sprite: Sprite) -> SpriteResumeDTO:
        return SpriteResumeDTO(id=sprite.id, path=sprite.path, size=sprite.size)
