from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class TagType(Base):
    __tablename__ = "tag_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exclusive = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # relacionamento
    tags = relationship("Tag", back_populates="tag_type")
