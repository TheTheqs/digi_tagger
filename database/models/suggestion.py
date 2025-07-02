# database/models/suggestion.py

from sqlalchemy import Column, Integer, Boolean, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

# Tabela associativa Many-to-Many entre Suggestion e Sprite
suggestion_sprites = Table(
    "suggestion_sprites",
    Base.metadata,
    Column("suggestion_id", Integer, ForeignKey("suggestions.id")),
    Column("sprite_id", Integer, ForeignKey("sprites.id")),
)

class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=True)
    verified = Column(Boolean, default=False)

    sprites = relationship("Sprite", secondary=suggestion_sprites, back_populates="suggestions")
