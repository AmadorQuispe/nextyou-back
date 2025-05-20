from uuid import UUID, uuid4
from datetime import datetime
from typing import List
from app.domain.journal_entry import JournalEntry
from app.application.port.outbound.journal_repository import JournalRepository
from app.infrastructure.db.postgres import Postgres

class PostgresJournalRepository(JournalRepository):
    def __init__(self, db: Postgres):
        self.db = db

    async def create(self, entry: JournalEntry) -> JournalEntry:
        query = """
            INSERT INTO journals (id, user_id, content, created_at)
            VALUES ($1, $2, $3, $4)
        """
        await self.db.execute(query, entry.id, entry.user_id, entry.content, entry.created_at)
        return entry
    
    async def update(self, entry: JournalEntry) -> JournalEntry:
        query = """
            UPDATE journals
            SET content = $2, updated_at = $3
            WHERE id = $1
        """
        await self.db.execute(query, entry.id, entry.content, entry.updated_at)
        return entry
    
    async def delete(self, entry_id: UUID) -> None:
        query = """
            DELETE FROM journals
            WHERE id = $1
        """
        await self.db.execute(query, entry_id)

    async def find_by_id(self, entry_id: UUID) -> JournalEntry | None:
        query = """
            SELECT id, user_id, content, created_at, updated_at
            FROM journals
            WHERE id = $1
        """
        row = await self.db.fetchrow(query, entry_id)
        if not row:
            return None
        return JournalEntry(**dict(row))

    async def find_by_user(self, user_id: UUID) -> List[JournalEntry]:
        query = """
            SELECT id, user_id, content, created_at, updated_at
            FROM journals
            WHERE user_id = $1
            ORDER BY created_at ASC
        """
        rows = await self.db.fetch(query, user_id)
        return [JournalEntry(**dict(row)) for row in rows]
