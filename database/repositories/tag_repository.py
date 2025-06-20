from database.models.tag import Tag

class TagRepository:
    def __init__(self, session):
        self.session = session

    def create(self, tag: Tag):
        self.session.add(tag)

    def delete(self, tag: Tag):
        self.session.delete(tag)

    def get_by_tag_type_id(self, tag_type_id: int) -> list[Tag]:
        return self.session.query(Tag).filter(Tag.tag_type_id == tag_type_id).all()