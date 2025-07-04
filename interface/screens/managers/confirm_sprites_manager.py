# interface/screens/managers/confirm_sprites_manager.py

from typing import List
from database.db_service import DBService
from database.dtos import SpriteResumeDTO


class ConfirmSpritesManager:
    def __init__(self, db: DBService):
        self.db = db
        self._tag_id: int | None = None
        self._tag_name: str = ""
        self._sprites: list[SpriteResumeDTO] = []

    def set_context(self, tag_id: int, tag_name: str, sprites: List[SpriteResumeDTO]):
        self._tag_id = tag_id
        self._tag_name = tag_name
        self._sprites = sprites.copy()  # cópia de segurança, caso precise restaurar original depois

    def get_tag_name(self) -> str:
        return self._tag_name

    def get_all_sprites(self) -> List[SpriteResumeDTO]:
        return self._sprites

    def remove_sprites_by_ids(self, sprite_ids: List[int]):
        self._sprites = [s for s in self._sprites if s.id not in sprite_ids]

    def save(self):
        if self._tag_id is None:
            raise ValueError("Tag não definida. Use set_context primeiro.")

        for sprite in self._sprites:
            self.db.add_tag_to_sprite(sprite.id, self._tag_id)
