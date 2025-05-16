from dataclasses import dataclass
import datetime


@dataclass
class JournalEntry:
    id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: datetime