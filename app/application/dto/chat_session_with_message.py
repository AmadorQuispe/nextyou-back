from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from app.domain.chat_message import ChatMessage


@dataclass
class ChatSessionWithMessages:
    id: UUID
    title: str
    started_at: datetime
    ended_at: datetime | None
    chat_messages: List[ChatMessage] | None