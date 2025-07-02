# database/models/embedding.py

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    sprite_id = Column(Integer, ForeignKey("sprites.id"), nullable=False)
    source = Column(String, nullable=False)  # ex: 'CLIP-ViT-B32'
    vector = Column(LargeBinary, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    sprite = relationship("Sprite", back_populates="embeddings")
