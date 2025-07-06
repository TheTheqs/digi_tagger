# database/repositories/sprite_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import select

from database.models.sprite import Sprite
from database.models.sprite_tag import SpriteTag
from database.models.tag import Tag


class SpriteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_sprite(self, path: str, vector: bytes, size: int) -> Sprite:
        # Verifica se o sprite já existe por path
        existing = self.session.query(Sprite).filter_by(path=path).first()
        if existing:
            print(f"[INFO] Sprite já existente para o path: {path}. Ignorando criação.")
            return existing
        print(f"[DEBUG] Tipo de subject.vector: {type(vector)}")
        print(f"[DEBUG] Início dos bytes: {vector[:10]}")
        sprite = Sprite(path=path, embeddings=vector, size=size)
        self.session.add(sprite)
        return sprite

    def get_by_id(self, sprite_id: int) -> Sprite | None:
        return self.session.query(Sprite).filter(Sprite.id == sprite_id).first()

    def get_by_tag_id(self, tag_id: int) -> list[Sprite]:
        return (
            self.session.query(Sprite)
            .join(Sprite.sprite_tags)
            .filter(SpriteTag.tag_id == tag_id)
            .all()
        )

    def add_tag(self, sprite_id: int, tag_id: int):
        exists = self.session.query(SpriteTag).filter_by(
            sprite_id=sprite_id,
            tag_id=tag_id
        ).first()
        if not exists:
            sprite_tag = SpriteTag(sprite_id=sprite_id, tag_id=tag_id)
            self.session.add(sprite_tag)

    def get_all(self) -> list[Sprite]:
        return self.session.query(Sprite).order_by(Sprite.size.asc()).all()

    def get_all_unlabeled_by_tag_type(self, tag_type_id: int) -> list[Sprite]:
        subquery = (
            select(Sprite.id)
            .join(Sprite.tags)
            .filter(Tag.tag_type_id == tag_type_id)
        )
        sprites = self.session.query(Sprite).filter(~Sprite.id.in_(subquery)).all()
        return sprites

    def get_sprite_id_by_paths(self, paths: list[str]) -> list[Sprite]:
        sprites = self.session.query(Sprite).filter(Sprite.path.in_(paths)).all()
        return sprites

    def has_tag_type(self, sprite_id: int, tag_type_id: int) -> bool:
        sprite = self.session.query(Sprite).filter(Sprite.id == sprite_id).first()
        if not sprite:
            return False
        return any(tag.tag_type_id == tag_type_id for tag in sprite.tags)

    def delete_all_sprites(self):
        self.session.query(Sprite).delete()
        print("[INFO] Todos os sprites foram removidos do banco.")

    def remove_all_sprite_tags(self):
        self.session.query(SpriteTag).delete()
        print("[INFO] Todas as tags associadas aos sprites foram removidas.")
