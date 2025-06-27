# database/repositories/sprite_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models.sprite import Sprite
from database.models.sprite_tag import SpriteTag

class SpriteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_sprite(self, path: str) -> Sprite:
        sprite = Sprite(path=path)
        self.session.add(sprite)
        return sprite

    def mark_sprite_as_edited(self, sprite_id: int):
        sprite = self.session.query(Sprite).filter(Sprite.id == sprite_id).first()
        if not sprite:
            raise ValueError(f"Sprite com ID {sprite_id} não encontrado.")
        sprite.edited = True

    def get_by_id(self, sprite_id: int) -> Sprite | None:
        return self.session.query(Sprite).filter(Sprite.id == sprite_id).first()

    def get_by_tag_id(self, tag_id: int) -> list[Sprite]:
        # busca por meio da tabela intermediária sprite_tags
        sprites = (
            self.session.query(Sprite)
            .join(Sprite.sprite_tags)
            .filter(SpriteTag.tag_id == tag_id)
            .all()
        )
        return sprites

    def add_tag(self, sprite_id: int, tag_id: int):
        from database.models.sprite_tag import SpriteTag

        # Verifica se já existe (pra evitar duplicata)
        exists = self.session.query(SpriteTag).filter_by(
            sprite_id=sprite_id,
            tag_id=tag_id
        ).first()

        if not exists:
            sprite_tag = SpriteTag(sprite_id=sprite_id, tag_id=tag_id)
            self.session.add(sprite_tag)

    def get_statistics(self) -> tuple[int, int, int]:
        total = self.session.query(func.count()).select_from(Sprite).scalar()
        edited = self.session.query(func.count()).select_from(Sprite).filter(Sprite.edited == True).scalar()
        unedited = self.session.query(func.count()).select_from(Sprite).filter(Sprite.edited == False).scalar()
        return total, edited, unedited

    def get_next_unedited(self) -> Sprite | None:
        return self.session.query(Sprite).filter_by(edited=False).first()