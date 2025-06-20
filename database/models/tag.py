from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base
from database.models.configuration_tags import configuration_tags

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # relacionamento
    tag_type = relationship("TagType", back_populates="tags")
    configurations = relationship("Configuration", secondary=configuration_tags, back_populates="tags")
