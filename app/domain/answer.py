from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Answer:
    id: UUID
    user_id: UUID
    question_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime | None = None