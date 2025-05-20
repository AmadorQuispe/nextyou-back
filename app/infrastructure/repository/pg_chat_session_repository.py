from typing import List
from uuid import UUID

from app.domain.chat_session import ChatSession
from app.application.port.outbound.chat_session_repository import ChatSessionRepository
from app.infrastructure.db.postgres import Postgres

class PostgresChatSessionRepository:
    def __init__(self, db: Postgres):
        self.db = db

    async def create(self, session: ChatSession) -> ChatSession:
        query = """
            INSERT INTO chat_sessions (id, user_id, title, started_at, ended_at)
            VALUES ($1, $2, $3, $4, $5)
        """
        await self.db.execute(query, session.id, session.user_id, session.title, session.started_at, session.ended_at)
        return session

    async def update(self, session: ChatSession) -> ChatSession:
        query = """
            UPDATE chat_sessions
            SET title = $2, ended_at = $3
            WHERE id = $1
        """
        await self.db.execute(query, session.id, session.title, session.ended_at)
        return session
    
    async def find_by_id(self, id: UUID) -> ChatSession | None:
        query = """
            SELECT id, user_id, title, started_at, ended_at
            FROM chat_sessions
            WHERE id = $1
        """
        row = await self.db.fetchrow(query, id)
        if not row:
            return None
        return ChatSession(**dict(row))

    async def find_all_by_user_id(self, user_id: UUID) -> list[ChatSession]:
        query = """
            SELECT id, user_id, title, started_at, ended_at
            FROM chat_sessions
            WHERE user_id = $1
        """
        rows = await self.db.fetch(query, user_id)
        return [ChatSession(**dict(row)) for row in rows]
    
    async def delete(self, id: UUID) -> None:
        query = """
            DELETE FROM chat_sessions
            WHERE id = $1
        """
        await self.db.execute(query, id)