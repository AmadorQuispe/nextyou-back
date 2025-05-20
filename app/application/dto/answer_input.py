
from dataclasses import dataclass
from uuid import UUID


@dataclass
class AnswerInput:
    question_id: UUID
    content: str
    