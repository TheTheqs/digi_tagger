from database.models.tag_type import TagType
from database.repositories.tag_type_repository import TagTypeRepository

class TagTypeService:
    def __init__(self, repository: TagTypeRepository):
        self.repository = repository

    def create(self, name: str):
        tag_type = TagType(name=name)
        self.repository.create(tag_type)
        return tag_type

    def delete(self, tag_type: TagType):
        self.repository.delete(tag_type)


    def get_tag_type_name(self, tag_type_id: int) -> str:
        return self.repository.get_tag_type_name(tag_type_id)

    def get_all_ids(self) -> list[int]:
        return self.repository.get_all_ids()