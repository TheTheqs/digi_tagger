from database.engine import SessionLocal
from database.models.tag_type import TagType
from database.models.tag import Tag
from database.models.sprite import Sprite
from database.repositories.tag_type_repository import TagTypeRepository
from database.repositories.tag_repository import TagRepository
from database.repositories.sprite_repository import SpriteRepository
from database.services.tag_type_service import TagTypeService
from database.services.tag_service import TagService
from database.services.sprite_service import SpriteService

class DbService:
    def __init__(self):
        self.session_factory = SessionLocal

    def create_tag_type(self, name: str, exclusive: bool) -> TagType:
        with self.session_factory() as session:
            tag_type_repo = TagTypeRepository(session)
            tag_type_service = TagTypeService(tag_type_repo)

            tag_type = tag_type_service.create(name, exclusive)
            session.commit()
            return tag_type

    def delete_tag_type(self, tag_type_id: int):
        with self.session_factory() as session:
            tag_type_repo = TagTypeRepository(session)
            tag_type = session.query(TagType).filter(TagType.id == tag_type_id).first()
            if not tag_type:
                raise ValueError("TagType não encontrado.")

            tag_type_service = TagTypeService(tag_type_repo)
            tag_type_service.delete(tag_type)
            session.commit()

    def create_tag(self, name: str, tag_type_id: int) -> Tag:
        with self.session_factory() as session:
            tag_repo = TagRepository(session)
            tag_service = TagService(tag_repo)

            # Valida se o TagType existe
            tag_type = session.query(TagType).filter(TagType.id == tag_type_id).first()
            if not tag_type:
                raise ValueError("TagType não encontrado.")

            tag = tag_service.create(name, tag_type)
            session.commit()
            return tag

    def get_tag_id_by_name(self, tag_name: str, tag_type: int) -> int:
        with self.session_factory() as session:
            tag_repo = TagRepository(session)
            tag_service = TagService(tag_repo)

            tag = tag_service.get_by_name_and_type(tag_name, tag_type)
            if not tag:
                raise ValueError("Tag não encontrada.")
            return tag.id

    def delete_tag(self, tag_id: int):
        with self.session_factory() as session:
            tag_repo = TagRepository(session)
            tag = session.query(Tag).filter(Tag.id == tag_id).first()
            if not tag:
                raise ValueError("Tag não encontrado.")

            tag_service = TagService(tag_repo)
            tag_service.delete(tag)
            session.commit()

    def get_tag_type_with_tags(self, tag_type_id: int) -> tuple[str, list[str]]:
        with self.session_factory() as session:
            tag_type_repo = TagTypeRepository(session)
            tag_repo = TagRepository(session)

            tag_type_service = TagTypeService(tag_type_repo)
            tag_service = TagService(tag_repo)

            tag_type = tag_type_service.get_tag_type_name(tag_type_id)
            tags = tag_service.get_by_tag_type_id(tag_type_id)
            tag_names = [tag.name for tag in tags]

            return tag_type, tag_names

    def get_all_tag_type_ids(self) -> list[int]:
        with self.session_factory() as session:
            tag_type_repo = TagTypeRepository(session)
            tag_type_service = TagTypeService(tag_type_repo)
            return tag_type_service.get_all_ids()

    def create_sprite(self, path: str) -> Sprite | None:
        with self.session_factory() as session:
            sprite_repo = SpriteRepository(session)
            sprite_service = SpriteService(sprite_repo)

            sprite = sprite_service.create_sprite(path)
            if sprite:  # Só faz commit se foi criado
                session.commit()
            return sprite

    def get_next_unedited_sprite(self) -> Sprite | None:
        with self.session_factory() as session:
            sprite_repo = SpriteRepository(session)
            sprite_service = SpriteService(sprite_repo)
            return sprite_service.get_next_unedited()

    def get_sprite_statistics(self) -> tuple[int, int, int]:
        with self.session_factory() as session:
            sprite_repo = SpriteRepository(session)
            sprite_service = SpriteService(sprite_repo)
            return sprite_service.get_complete_data()
