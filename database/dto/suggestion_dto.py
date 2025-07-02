# database/dto/suggestionDTO.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SuggestionDTO:
    sprite_indices: List[int]  # posição dos sprites na lista original
    description: Optional[str] = None
    verified: bool = False
