# database/dto/suggestionDTO.py

from dataclasses import dataclass
from typing import List

@dataclass
class SuggestionDTO:
    suggestion_id: int
    sprite_paths: List[str]
