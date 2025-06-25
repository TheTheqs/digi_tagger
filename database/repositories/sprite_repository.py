# database/repositories/sprite_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models.sprite import Sprite
from database.models.configuration import Configuration
from sqlalchemy.orm import joinedload

class SpriteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_sprite(self, path: str) -> Sprite:
        sprite = Sprite(path=path)
        self.session.add(sprite)
        return sprite

    def exist_by_path(self, path: str) -> bool:
        exists = self.session.query(Sprite).filter(Sprite.path == path).first()
        return exists is not None

    def get_next_unedited(self) -> Sprite | None:
        sprite = self.session.query(Sprite).filter(Sprite.edited == False).first()
        return sprite

    def get_complete_data(self) -> tuple[int, int, int]:
        total = self.session.query(func.count(Sprite.id)).scalar()
        edited = self.session.query(func.count(Sprite.id)).filter(Sprite.edited == True).scalar()
        unedited = self.session.query(func.count(Sprite.id)).filter(Sprite.edited == False).scalar()
        return total, edited, unedited

    def get_by_id(self, sprite_id: int) -> Sprite | None:
        return self.session.query(Sprite).filter(Sprite.id == sprite_id).first()

    def update_sprite_with_configuration(self, sprite: Sprite, configuration: Configuration):
        sprite.configuration = configuration
        sprite.edited = True

    def get_all_edited_ids(self) -> list[int]:
        result = self.session.query(Sprite.id).filter(Sprite.edited == True).all()
        return [r[0] for r in result]