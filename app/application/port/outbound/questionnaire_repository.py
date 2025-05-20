
from abc import ABC
from typing import List
from uuid import UUID
from app.domain.questionnaire import Questionnaire


class QuestionnaireRepository(ABC):
    def find_all(self) -> List[Questionnaire]:
        ...
    
    def find_by_id(self, id: UUID) -> Questionnaire | None:
        ...