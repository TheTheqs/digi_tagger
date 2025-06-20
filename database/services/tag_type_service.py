from database.models.tag_type import TagType
from database.repositories.tag_type_repository import TagTypeRepository

class TagTypeService:
    def __init__(self, repository: TagTypeRepository):
        self.repository = repository

    def create(self, name: str, exclusive: bool):
        tag_type = TagType(name=name, exclusive=exclusive)
        self.repository.create(tag_type)
        return tag_type

    def delete(self, tag_type: TagType):
        self.repository.delete(tag_type)
