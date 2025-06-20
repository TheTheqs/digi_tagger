from database.models.tag import Tag
from database.models.tag_type import TagType
from database.repositories.tag_repository import TagRepository

class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    def create(self, name: str, tag_type: TagType):
        tag = Tag(name=name, tag_type=tag_type)
        self.repository.create(tag)
        return tag

    def delete(self, tag: Tag):
        self.repository.delete(tag)
