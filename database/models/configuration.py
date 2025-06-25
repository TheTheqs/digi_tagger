# database/models/configuration.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relacionamentos
    sprites = relationship("Sprite", back_populates="configuration")
    tags = relationship("Tag", secondary="configuration_tags", back_populates="configurations")
