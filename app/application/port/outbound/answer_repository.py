
from typing import List, Protocol
from uuid import UUID

from app.domain.answer import Answer


class AnswerRepository(Protocol):
    def save(self, answer: Answer) -> Answer:
        ...
    def save_batch(self, answers: List[Answer]) -> List[Answer]:
        ...
    def find_all_by_user_id(self, user_id: UUID) -> List[Answer]:
        ...        
    def find_by_id(self, answer_id: UUID) -> Answer | None:
        ...
    def count_by_user(self, user_id: UUID) -> int:
        ...
    