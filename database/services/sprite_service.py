# database/services/sprite_service.py
from database.models.configuration import Configuration
from database.repositories.sprite_repository import SpriteRepository
from database.models.sprite import Sprite

class SpriteService:
    def __init__(self, sprite_repository: SpriteRepository):
        self.sprite_repository = sprite_repository

    def create_sprite(self, path: str) -> Sprite | None:
        if self.sprite_repository.exist_by_path(path):
            print(f"[LOG] Sprite já existente no banco com path: {path}")
            return None  # Não cria duplicata
        sprite = self.sprite_repository.create_sprite(path)
        return sprite

    def get_next_unedited(self) -> Sprite | None:
        return self.sprite_repository.get_next_unedited()

    def get_complete_data(self) -> tuple[int, int, int]:
        return self.sprite_repository.get_complete_data()

    def get_by_id(self, sprite_id: int) -> Sprite|None:
        return self.sprite_repository.get_by_id(sprite_id)

    def update_sprite_with_configuration(self, sprite: Sprite, configuration: Configuration):
        self.sprite_repository.update_sprite_with_configuration(sprite, configuration)

    def get_all_edited_id(self) -> list[int]:
        return self.sprite_repository.get_all_edited_ids()