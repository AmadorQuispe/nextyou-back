from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Question:
    id: UUID 
    questionnaire_id: UUID
    prompt: str
    helper: str
    position: int
    created_at: datetime
    updated_at: datetime | None

    