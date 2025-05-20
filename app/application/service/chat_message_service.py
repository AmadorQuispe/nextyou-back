from typing import List
import uuid
import datetime as dt
from app.application.port.inbound.chat_message_use_case import ChatMessageUseCase
from app.application.port.outbound.chat_message_repository import ChatMessageRepository
from app.domain.chat_message import ChatMessage

class ChatMessageService:
    def __init__(self, chat_message_repository: ChatMessageRepository):
        self.chat_message_repository = chat_message_repository

    async def create(self,session_id: uuid.UUID,sender:str, message: str) -> ChatMessage:
        new_message = ChatMessage(
            id=uuid.uuid4(),
            session_id=session_id, 
            sender=sender, 
            content=message, 
            send_at=dt.datetime.now(tz=dt.timezone.utc)
        )
        await self.chat_message_repository.create(new_message)
        return new_message
    
    async def get_by_session(self, session_id: uuid.UUID) -> List[ChatMessage]:
        return await self.chat_message_repository.find_by_session(session_id)