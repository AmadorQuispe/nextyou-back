from typing import List
from uuid import UUID

from app.domain.chat_message import ChatMessage
from app.application.port.outbound.chat_message_repository import ChatMessageRepository
from app.infrastructure.db.postgres import Postgres

class PostgresChatMessageRepository:
    def __init__(self, db: Postgres):
        self.db = db

    async def create(self, message: ChatMessage) -> ChatMessage:
        query = """
            INSERT INTO chat_messages (id, session_id, sender, content, send_at)
            VALUES ($1, $2, $3, $4, $5)
        """
        await self.db.execute(query, message.id, message.session_id, message.sender, message.content, message.send_at)
        return message
    
    async def find_by_session(self,session_id: UUID) -> List[ChatMessage]:
        query = """
            SELECT id, session_id, sender, content, send_at
            FROM chat_messages
            WHERE session_id = $1 ORDER BY send_at ASC
        """
        rows = await self.db.fetch(query, session_id)
        return [ChatMessage(**dict(row)) for row in rows]