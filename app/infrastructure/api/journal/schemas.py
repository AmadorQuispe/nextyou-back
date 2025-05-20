from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JournalEntryCreate(BaseModel):
    content: str

class JournalEntryUpdate(BaseModel):
    id: UUID
    content: str

class JournalEntryResponse(BaseModel):
    id: UUID
    user_id: UUID
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
