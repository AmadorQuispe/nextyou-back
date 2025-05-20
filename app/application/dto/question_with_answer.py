
from dataclasses import dataclass
from uuid import UUID

from app.domain.answer import Answer


@dataclass
class QuestionWithAnswer:
    id: UUID 
    questionnaire_id: UUID
    prompt: str
    helper: str
    position: int
    answer: Answer | None