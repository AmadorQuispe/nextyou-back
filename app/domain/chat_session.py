from dataclasses import dataclass
import datetime

@dataclass
class ChatSession:
    id: str
    user_id: str
    title: str
    started_at: datetime
    ended_at: datetime