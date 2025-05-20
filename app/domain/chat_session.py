from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class ChatSession:
    id: UUID
    user_id: UUID
    title: str
    started_at: datetime
    ended_at: datetime | None