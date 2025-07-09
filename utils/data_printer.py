from database.db_service import DBService
from database.dtos import TagResponseDTO, TagTypeResponseDTO


class DataPrinter:
    def __init__(self, db: DBService):
        self.db = db

    def print_data(self):
        tags: list[TagResponseDTO] = self.db.get_all_tags()
        for tag in tags:
            print("id: " + str(tag.id) + " " + self.build_name(tag).name + ": " + str(len(tag.sprites)))

    def build_name(self, tag: TagResponseDTO) -> TagResponseDTO:
        tag_type: TagTypeResponseDTO = self.db.get_tag_type_by_id(tag.tag_type_id)
        tag.name = tag_type.name + "_" + tag.name
        return tag

