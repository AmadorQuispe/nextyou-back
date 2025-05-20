from dataclasses import dataclass
from typing import Optional
from uuid import UUID
import datetime as dt


@dataclass
class JournalEntry:
    id: UUID
    user_id: UUID
    content: str
    created_at: dt.datetime
    updated_at: Optional[dt.datetime] = None

    def update_content(self, new_content: str):
        self.content = new_content
        self.updated_at = dt.datetime.now(tz=dt.timezone.utc)