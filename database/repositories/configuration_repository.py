# database/repositories/configuration_repository.py

from sqlalchemy.orm import Session
from database.models.configuration import Configuration
from database.models.tag import Tag

class ConfigurationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_configuration(self, name: str, tags: list[Tag]) -> Configuration:
        for tag in tags:
            print(tag.tag_type.name + ": " + tag.name)
        configuration = Configuration(name=name)
        configuration.tags = tags  # ORM já associa na tabela intermediária
        self.session.add(configuration)
        return configuration

    def get_by_sprite_id(self, sprite_id: int) -> Configuration | None:
        return self.session.query(Configuration).filter(Configuration.sprites.any(id=sprite_id)).first()