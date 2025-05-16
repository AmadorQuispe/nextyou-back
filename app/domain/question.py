from dataclasses import dataclass

@dataclass
class Question:
    id: str
    questionnaire_id: str
    prompt: str
    helper: str
    order: int

    