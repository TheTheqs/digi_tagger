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

    def get_all_sprite_id_paths(self) -> list[tuple[int, str]]:
        sprites = self.session.query(Sprite.id, Sprite.path).all()
        return sprites

    def get_all_unlabeled_by_tag_type(self, tag_type_id: int) -> list[tuple[int, str]]:
        # Subquery: todos os sprite_ids com pelo menos uma tag do tipo fornecido
        from database.models.tag import Tag
        from sqlalchemy import select

        subquery = (
            select(Sprite.id)
            .join(Sprite.tags)
            .filter(Tag.tag_type_id == tag_type_id)
        )

        # Query principal: pega os sprites que não estão na subquery
        sprites = (
            self.session.query(Sprite.id, Sprite.path)
            .filter(~Sprite.id.in_(subquery))
            .all()
        )

        return sprites

    def get_sprite_id_by_paths(self, paths: list[str]) -> list[tuple[int, str]]:
        sprites = (
            self.session.query(Sprite.id, Sprite.path)
            .filter(Sprite.path.in_(paths))
            .all()
        )
        return sprites

    def has_tag_type(self, sprite_id: int, tag_type_id: int) -> bool:
        sprite = self.session.query(Sprite).filter(Sprite.id == sprite_id).first()
        if not sprite:
            return False
        for tag in sprite.tags:
            if tag.tag_type_id == tag_type_id:
                return True
        return False