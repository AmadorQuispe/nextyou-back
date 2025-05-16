from dataclasses import dataclass
import datetime

@dataclass
class ChatMessage:
    id: str
    session_id: str
    sender: str
    content: str
    created_at: datetime
