# database/repositories/suggestion_repository.py

from sqlalchemy.orm import Session
from database.models.suggestion import Suggestion
from database.dto.suggestion_response_dto import SuggestionDTO

class SuggestionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, suggestion: Suggestion):
        self.session.add(suggestion)

    def get_next_unverified_dto(self) -> SuggestionDTO | None:
        suggestion = (
            self.session.query(Suggestion)
            .filter(Suggestion.verified == False)
            .first()
        )
        if suggestion is None:
            return None

        paths = [sprite.path for sprite in suggestion.sprites]
        return SuggestionDTO(suggestion_id=suggestion.id, sprite_paths=paths)

    def mark_verified(self, suggestion_id: int):
        suggestion = self.session.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
        if suggestion:
            suggestion.verified = True

    def count_total_suggestions(self) -> int:
        return self.session.query(Suggestion).count()