from typing import List, Protocol
from uuid import UUID

from app.domain.chat_message import ChatMessage


class ChatMessageUseCase(Protocol):
    def create(self,session_id: UUID,sender:str, message: str) -> ChatMessage:
        ...
    def get_by_session(self, session_id: UUID) -> List[ChatMessage]:
        ...