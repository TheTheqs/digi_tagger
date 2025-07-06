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

    def get_all(self) -> list[TagType]:
        return self.session.query(TagType).all()

    def get_by_name(self, name: str) -> TagType | None:
        return self.session.query(TagType).filter(TagType.name == name).first()

    def delete_all(self):
        tags = self.session.query(TagType).all()
        for tag in tags:
            self.session.delete(tag)
