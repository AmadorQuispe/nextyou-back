
from abc import ABC
from typing import List
from uuid import UUID
from app.domain.question import Question


class QuestionRepository(ABC):
    def find_all(self) -> List[Question]:
        ...
    
    def find_by_id(self, id: UUID) -> Question | None:
        ...
    
    