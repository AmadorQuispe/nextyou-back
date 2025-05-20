
from typing import List, Protocol
from uuid import UUID
from datetime import datetime

from app.domain.chat_message import ChatMessage

class ChatMessageRepository(Protocol):
    def create(self, message: ChatMessage) -> ChatMessage:
        ...

    def find_by_session(self, session_id: UUID) -> List[ChatMessage]:
        ...
