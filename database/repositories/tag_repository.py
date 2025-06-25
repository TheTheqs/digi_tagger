# database/repositories/tag_repository.py
from database.models.tag import Tag
from sqlalchemy import and_

class TagRepository:
    def __init__(self, session):
        self.session = session

    def create(self, tag: Tag):
        self.session.add(tag)

    def delete(self, tag: Tag):
        self.session.delete(tag)

    def get_by_id(self, tag_id: int) -> Tag|None:
        return self.session.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_tag_type_id(self, tag_type_id: int) -> list[Tag]:
        return self.session.query(Tag).filter(Tag.tag_type_id == tag_type_id).all()

    def get_by_name_and_type(self, tag_name: str, tag_type_id: int) -> Tag | None:
        tag: Tag = self.session.query(Tag).filter(
            and_(
                Tag.name == tag_name,
                Tag.tag_type_id == tag_type_id
            )
        ).first()

        if not tag:
            raise ValueError("Tag não encontrada.")

        return tag