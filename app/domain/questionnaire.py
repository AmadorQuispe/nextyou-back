from dataclasses import dataclass


@dataclass
class Questionnaire:
    id: str
    title: str
    description: str
    order: int
