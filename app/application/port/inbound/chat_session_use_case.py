from typing import List, Protocol
from uuid import UUID

from app.application.dto.chat_session_with_message import ChatSessionWithMessages
from app.domain.chat_session import ChatSession


class ChatSessionUseCase(Protocol):
    def create(self, user_id: UUID, title: str) -> ChatSession:
        ...
    def get_all_by_user(self, user_id: UUID) -> List[ChatSession]:
        ...
    def get_by_id(self, session_id: UUID,tree: bool = False) -> ChatSessionWithMessages:
        ...
    def update(self, session_id: UUID, title: str) -> ChatSession:
        ...
    def delete(self, session_id: UUID) -> None:
        ...