from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Questionnaire:
    id: UUID
    title: str
    description: str
    position: int
    created_at: datetime
