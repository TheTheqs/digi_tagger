# database/models/sprite_tag.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class SpriteTag(Base):
    __tablename__ = "sprite_tags"

    id = Column(Integer, primary_key=True)
    sprite_id = Column(Integer, ForeignKey("sprites.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("sprite_id", "tag_id", name="_sprite_tag_uc"),)

    sprite = relationship("Sprite", back_populates="sprite_tags", overlaps="tags,sprites")
    tag = relationship("Tag", back_populates="sprite_tags", overlaps="tags,sprites")

