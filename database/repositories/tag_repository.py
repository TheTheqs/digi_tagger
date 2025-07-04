# database/repositories/tag_repository.py

from sqlalchemy.orm import Session
from database.models.tag import Tag

class TagRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag_type_id: int, name: str, description: str):
        tag: Tag = Tag(name=name, description=description, tag_type_id=tag_type_id)
        self.session.add(tag)

    def delete(self, tag: Tag):
        self.session.delete(tag)

    def get_by_tag_type_id(self, tag_type_id: int) -> list[Tag]:
        return self.session.query(Tag).filter(Tag.tag_type_id == tag_type_id).all()

    def get_by_id(self, tag_id: int) -> Tag | None:
        return self.session.query(Tag).filter(Tag.id == tag_id).first()

    def get_all(self) -> list[Tag]:
        return self.session.query(Tag).all()

    def delete_all(self):
        tags = self.session.query(Tag).all()
        for tag in tags:
            self.session.delete(tag)
