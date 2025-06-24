# database/services/sprite_service.py

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
