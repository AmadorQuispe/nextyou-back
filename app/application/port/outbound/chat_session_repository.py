
from typing import Protocol
from uuid import UUID
from datetime import datetime

from app.domain.chat_session import ChatSession

class ChatSessionRepository(Protocol):
    def create(self, session: ChatSession) -> ChatSession:
        ...
    
    def update(self, session: ChatSession) -> ChatSession:
        ...

    def find_by_id(self, id: UUID) -> ChatSession | None:
        ...

    def find_all_by_user_id(self, user_id: UUID) -> list[ChatSession]:
        ...

    def delete(self, id: UUID) -> None: 
        ...