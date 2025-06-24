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

    def get_by_tag_type_id(self, tag_type_id: int) -> list[Tag]:
        return self.repository.get_by_tag_type_id(tag_type_id)

    def get_by_name_and_type(self, tag_name, tag_type: int) -> Tag|None:
        return self.repository.get_by_name_and_type(tag_name, tag_type)