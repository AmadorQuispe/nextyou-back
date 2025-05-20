
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class ChatMessage(BaseModel):
    id: UUID
    sender: str
    content: str
    send_at: datetime

class ChatSessionResponse(BaseModel):
    id: UUID
    title: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    chat_messages: Optional[List[ChatMessage]] = None

class ChatSessionRequest(BaseModel):
    title: str

