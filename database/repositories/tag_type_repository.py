# database/repositories/tag_type_repository.py

from sqlalchemy.orm import Session
from database.models.tag_type import TagType

class TagTypeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag_type: TagType):
        self.session.add(tag_type)

    def delete(self, tag_type: TagType):
        self.session.delete(tag_type)

    def get_by_id(self, tag_type_id: int) -> TagType | None:
        return self.session.query(TagType).filter(TagType.id == tag_type_id).first()

    def get_all_id_name_pairs(self) -> list[tuple[str, int]]:
        return self.session.query(TagType.name, TagType.id).all()
