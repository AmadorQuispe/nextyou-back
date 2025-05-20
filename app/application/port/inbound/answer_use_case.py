from typing import List, Protocol, TypedDict
from uuid import UUID
from app.application.dto.answer_input import AnswerInput
from app.domain.answer import Answer



class AnswerUseCase(Protocol):
    def create(self, user_id: UUID, question_id: UUID, content: str) -> Answer:
        ...
    def create_batch(self, user_id: UUID, answers: List[AnswerInput]) -> List[Answer]:
        ...
    def update(self,user_id: UUID, answer_id: UUID, content: str) -> Answer:
        ...
    def get_by_user(self, user_id: UUID) -> List[Answer]:
        ...
    def count_by_user(self, user_id: UUID) -> int:
        ...