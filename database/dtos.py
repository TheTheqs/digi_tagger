# database/dtos.py

from dataclasses import dataclass
from typing import List

# TAG TYPE
@dataclass
class TagTypeRequestDTO:
    name: str

@dataclass
class TagTypeResponseDTO:
    id: int
    name: str

# TAG
@dataclass
class TagRequestDTO:
    tag_type_id: int
    name: str
    description: str

@dataclass
class SpriteResumeDTO:
    id: int
    path: str
    size: int

@dataclass
class TagResponseDTO:
    id: int
    tag_type_id: int
    name: str
    description: str
    sprites: List[SpriteResumeDTO]

# Sprite
@dataclass
class SpriteRequestDTO:
    path: str
    vector: bytes
    size: int

@dataclass
class TagResumeDTO:
    id: int
    name: str
    tag_type_id: int

@dataclass
class SpriteResponseDTO:
    id: int
    path: str
    vector: bytes
    size: int
    tags: List[TagResumeDTO]