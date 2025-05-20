import uuid
import datetime as dt
from typing import List
from app.application.dto.chat_session_with_message import ChatSessionWithMessages
from app.application.port.inbound.chat_message_use_case import ChatMessageUseCase
from app.application.port.inbound.chat_session_use_case import ChatSessionUseCase
from app.application.port.outbound.chat_session_repository import ChatSessionRepository
from app.domain.chat_session import ChatSession

class ChatSessionService:
    def __init__(
            self, 
            chat_session_repository: ChatSessionRepository,
            chat_message_use_case: ChatMessageUseCase
        ):
        self.chat_session_repository = chat_session_repository
        self.chat_message_use_case = chat_message_use_case

    async def create(self, user_id: uuid.UUID, title: uuid.UUID) -> ChatSession:
        new_session = ChatSession(
            id=uuid.uuid4(), 
            user_id=user_id, 
            title=title, 
            started_at=dt.datetime.now(tz=dt.timezone.utc),
            ended_at=None
        )
        await self.chat_session_repository.create(new_session)
        return new_session


    async def get_all_by_user(self, user_id: uuid.UUID) -> List[ChatSession]:
        all_sessions = await self.chat_session_repository.find_all_by_user_id(user_id)
        return all_sessions

    async def get_by_id(self, session_id:uuid.UUID,tree: bool = False) -> ChatSessionWithMessages:
        session = await self.chat_session_repository.find_by_id(session_id)
        
        if not tree:
            return ChatSessionWithMessages(
                id=session.id,
                title=session.title,
                started_at=session.started_at,
                ended_at=session.ended_at,
                chat_messages=None
            )
        messages = await self.chat_message_use_case.get_by_session(session_id)
        return ChatSessionWithMessages(
            id=session.id,
            title=session.title,
            started_at=session.started_at,
            ended_at=session.ended_at,
            chat_messages=messages
        )


    async def update(self, session_id: uuid.UUID, title: str) -> ChatSession:
        session = await self.chat_session_repository.find_by_id(session_id)
        session.title = title
        await self.chat_session_repository.update(session)
        return session


    async def delete(self, session_id: uuid.UUID) -> None:
        await self.chat_session_repository.delete(session_id)