# database/repositories/tag_repository.py

from sqlalchemy.orm import Session
from database.models.tag import Tag

class TagRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag: Tag):
        self.session.add(tag)

    def delete(self, tag: Tag):
        self.session.delete(tag)

    def get_tag_id_name_by_tag_type_id(self, tag_type_id: int) -> list[tuple[str, int]]:
        return [
            (tag.name, tag.id)
            for tag in self.session.query(Tag)
            .filter(Tag.tag_type_id == tag_type_id)
            .all()
        ]

    def get_by_id(self, tag_id: int) -> Tag | None:
        return self.session.query(Tag).filter(Tag.id == tag_id).first()