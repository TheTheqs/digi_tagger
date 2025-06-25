# database/services/configuration_service.py

from database.repositories.configuration_repository import ConfigurationRepository
from database.repositories.tag_repository import TagRepository
from database.models.configuration import Configuration

class ConfigurationService:
    def __init__(self, configuration_repository: ConfigurationRepository, tag_repository: TagRepository):
        self.configuration_repository = configuration_repository
        self.tag_repository = tag_repository

    def create_configuration(self, name: str, tag_ids: list[int]) -> Configuration:
        tags = []
        for tag_id in tag_ids:
            tag = self.tag_repository.get_by_id(tag_id)
            if not tag:
                print(f"[LOG] Tag não encontrada: ID {tag_id}")
                continue
            tags.append(tag)

        if len(tags) != len(tag_ids):
            print(f"[LOG] Algumas tags não foram encontradas no banco.")

        # Ordenação pelo tag_type_id
        tags.sort(key=lambda tag: tag.tag_type_id)

        configuration = self.configuration_repository.create_configuration(name, tags)
        return configuration

    def get_by_sprite_id(self, sprite_id: int) -> Configuration| None:
        return self.configuration_repository.get_by_sprite_id(sprite_id)