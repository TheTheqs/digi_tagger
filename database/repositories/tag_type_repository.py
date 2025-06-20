from database.models.tag_type import TagType

class TagTypeRepository:
    def __init__(self, session):
        self.session = session

    def create(self, tag_type: TagType):
        self.session.add(tag_type)

    def delete(self, tag_type: TagType):
        self.session.delete(tag_type)
