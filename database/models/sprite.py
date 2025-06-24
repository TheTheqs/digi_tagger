# database/models/sprite.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class Sprite(Base):
    __tablename__ = "sprites"

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    edited = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # relacionamento
    configuration_id = Column(Integer, ForeignKey("configurations.id"))
    configuration = relationship("Configuration", back_populates="sprites")
