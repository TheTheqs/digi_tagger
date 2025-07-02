# database/models/sprite.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base
from database.models.embedding import Embedding
from database.models.suggestion import suggestion_sprites


class Sprite(Base):
    __tablename__ = "sprites"

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    sprite_tags = relationship("SpriteTag", back_populates="sprite", cascade="all, delete-orphan", overlaps="tags")
    tags = relationship("Tag", secondary="sprite_tags", back_populates="sprites", overlaps="sprite_tags")

    suggestions = relationship("Suggestion", secondary=suggestion_sprites, back_populates="sprites")

    embeddings = relationship(Embedding, back_populates="sprite")