# interface/screens/managers/tagging_data_manager.py

from database.dtos import (
    TagTypeResponseDTO, TagResponseDTO, SpriteResumeDTO,
    TagTypeRequestDTO, TagRequestDTO, SpriteResponseDTO
)
from database.db_service import DBService
from services.assisted_curation_service import AssistedCurationService

class TaggingDataManager:
    def __init__(self, db: DBService, assist: AssistedCurationService):
        self.db = db
        self.assist = assist
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

    def get_unlabeled_sprites(self, tag_type_id: int) -> list[SpriteResumeDTO]:
        if tag_type_id == -1:
            return self.get_all_sprites()
        return [
            sprite for sprite in self._all_sprites
            if not self._sprite_has_tag_type(sprite.id, tag_type_id)
        ]

    def _sprite_has_tag_type(self, sprite_id: int, tag_type_id: int) -> bool:
        for tag in self._tags_by_type.get(tag_type_id, []):
            if any(s.id == sprite_id for s in tag.sprites):
                return True
        return False

    def sort_sprites(self, sprites: list[SpriteResumeDTO]) -> list[SpriteResumeDTO]:
        return sorted(sprites, key= lambda s: s.size)

    # --- TagTypes ---
    def get_all_tag_types(self) -> list[TagTypeResponseDTO]:
        return self._tag_types

    def refresh_tag_type_list(self):
        self._tag_types = self.db.get_all_tag_types()

    def create_tag_type(self, name: str) -> TagTypeResponseDTO:
        tag_type = self.db.create_tag_type(TagTypeRequestDTO(name))
        self.refresh_tag_type_list()
        return tag_type

    # --- Tags ---
    def get_tags_by_tag_type(self, tag_type_id: int) -> list[TagResponseDTO]:
        return self._tags_by_type.get(tag_type_id, [])

    def refresh_tag_list(self, tag_type_id: int):
        self._tags_by_type[tag_type_id] = self.db.get_tags_by_tag_type(tag_type_id)

    def create_tag(self, tag_type_id: int, name: str, description: str) -> TagResponseDTO:
        tag = self.db.create_tag(TagRequestDTO(tag_type_id, name, description))
        self.refresh_tag_list(tag_type_id)
        self._all_tags_flat = [tag for tags in self._tags_by_type.values() for tag in tags]
        return tag

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

    # --- Curadoria assistida com RANK ---
    def get_top_k_curated_sprites_by_tag(
        self,
        tag_id: int,
        sprites: list[SpriteResponseDTO],
        top_k: int = 10
    ) -> list[SpriteResponseDTO]:
        tag = self.get_tag_by_id(tag_id)
        if not tag:
            return []

        return self.assist.get_top_k_similar(tag.description, sprites, top_k=top_k)