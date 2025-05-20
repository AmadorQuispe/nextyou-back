
from dataclasses import dataclass
from typing import List
from uuid import UUID

from app.application.dto.question_with_answer import QuestionWithAnswer


@dataclass
class QuestionnaireWithQuestionsAndAnswers:
    id: UUID
    title: str
    description: str
    position: int
    questions: List[QuestionWithAnswer]
    