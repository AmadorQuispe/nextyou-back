from dataclasses import dataclass
import datetime
from uuid import UUID

@dataclass
class ChatMessage:
    id: UUID
    session_id: UUID
    sender: str # ENUM ['user', 'assistant']
    content: str
    send_at: datetime
