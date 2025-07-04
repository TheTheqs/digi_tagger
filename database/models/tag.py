# database/models/tag.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    tag_type_id = Column(Integer, ForeignKey("tag_types.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    tag_type = relationship("TagType", back_populates="tags")
    sprite_tags = relationship("SpriteTag", back_populates="tag", cascade="all, delete-orphan", overlaps="sprites")
    sprites = relationship("Sprite", secondary="sprite_tags", back_populates="tags", overlaps="sprite_tags")

