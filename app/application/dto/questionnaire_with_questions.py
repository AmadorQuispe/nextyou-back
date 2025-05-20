from dataclasses import dataclass
from typing import List
from uuid import UUID

from app.domain.question import Question

@dataclass
class QuestionnaireWithQuestions:
    id: UUID
    title: str
    description: str
    position: int
    questions: List[Question]