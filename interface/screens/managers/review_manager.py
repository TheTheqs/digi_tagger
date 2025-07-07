# interface/screens/managers/review_manager.py

from database.dtos import (
    TagTypeResponseDTO, TagResponseDTO, SpriteResumeDTO
)
from database.db_service import DBService

class ReviewManager:
    def __init__(self, db: DBService):
        self.db = db
        self._all_sprites: list[SpriteResumeDTO] = []
        self._tag_types: list[TagTypeResponseDTO] = []
        self._tags_by_type: dict[int, list[TagResponseDTO]] = {}
        self._all_tags_flat: list[TagResponseDTO] = []

    def load_all(self):
        self._all_sprites = self.db.get_all_sprites()
        self._tag_types = self.db.get_all_tag_types()
        self._tags_by_type = {
            tt.id: self.db.get_tags_by_tag_type(tt.id)
            for tt in self._tag_types
        }
        self._all_tags_flat = [tag for tags in self._tags_by_type.values() for tag in tags]

    # --- Sprites ---
    def get_all_sprites(self) -> list[SpriteResumeDTO]:
        return self._all_sprites

    def remove_tag(self, sprite_ids: list[int], tag_id: int):
        if tag_id == -1 or len(sprite_ids) == 0:
            return
        for sprite_id in sprite_ids:
            self.db.remove_tag_from_sprite(sprite_id, tag_id)
        self.load_all()

    # --- TagTypes ---
    def get_all_tag_types(self) -> list[TagTypeResponseDTO]:
        return self._tag_types

    def refresh_tag_type_list(self):
        self._tag_types = self.db.get_all_tag_types()

    # --- Tags ---
    def get_tags_by_tag_type(self, tag_type_id: int) -> list[TagResponseDTO]:
        return self._tags_by_type.get(tag_type_id, [])

    def refresh_tag_list(self, tag_type_id: int):
        self._tags_by_type[tag_type_id] = self.db.get_tags_by_tag_type(tag_type_id)

    def get_tag_by_id(self, tag_id: int) -> TagResponseDTO | None:
        return next((t for t in self._all_tags_flat if t.id == tag_id), None)

    # --- Dropdowns ---
    def get_tag_dropdown_options(self) -> list[tuple[str, int]]:
        return [(f"{self._get_tag_type_name(tag)}_{tag.name}", tag.id) for tag in self._all_tags_flat]

    def get_tag_dropdown_options_excluding_type(self, excluded_tag_type_id: int) -> list[tuple[str, int]]:
        return [
            (f"{self._get_tag_type_name(tag)}_{tag.name}", tag.id)
            for tag in self._all_tags_flat
            if tag.tag_type_id != excluded_tag_type_id
        ]

    def _get_tag_type_name(self, tag: TagResponseDTO) -> str:
        tt = next((t for t in self._tag_types if t.id == tag.tag_type_id), None)
        return tt.name if tt else "?"