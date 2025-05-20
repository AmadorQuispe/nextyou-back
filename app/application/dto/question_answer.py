
from dataclasses import dataclass


@dataclass
class QuestionAnswer:
    question_id: str
    questionnaire: str
    question: str
    answer: str
