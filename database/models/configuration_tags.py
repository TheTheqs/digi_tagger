from sqlalchemy import Column, Integer, ForeignKey, Table
from database.base import Base

configuration_tags = Table(
    "configuration_tags",
    Base.metadata,
    Column("configuration_id", Integer, ForeignKey("configurations.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)
