from database.models.tag import Tag

class TagRepository:
    def __init__(self, session):
        self.session = session

    def create(self, tag: Tag):
        self.session.add(tag)

    def delete(self, tag: Tag):
        self.session.delete(tag)
