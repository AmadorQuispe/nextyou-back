

from typing import List
from uuid import UUID
from app.application.port.outbound.journal_repository import JournalRepository
from app.domain.journal_entry import JournalEntry
import uuid
import datetime as dt

class JournalService:
    def __init__(self, repository: JournalRepository):
        self.repository = repository
        
    def get_all_by_user(self, user_id: UUID) -> List[JournalEntry]:
        return self.repository.find_by_user(user_id)

    async def add_entry(self, user_id: UUID, content: str) -> JournalEntry:
        entry = JournalEntry(
            id=uuid.uuid4(),
            user_id=user_id,
            content=content,
            created_at=dt.datetime.now(tz=dt.timezone.utc),
            updated_at=dt.datetime.now(tz=dt.timezone.utc),
        )
        await self.repository.create(entry)
        return entry
    
    async def update_entry(self, entry_id: UUID, new_content: str ) -> JournalEntry:
        if not entry_id:
            raise ValueError("Entry ID is required")
        
        entryInDb = await self.repository.find_by_id(entry_id)

        if not entryInDb:
            raise ValueError("Entry not found")

        entry = JournalEntry(
            id=entryInDb.id,
            user_id=entryInDb.user_id,
            content=new_content,
            created_at=entryInDb.created_at,
            updated_at=dt.datetime.now(tz=dt.timezone.utc),
        )
        await self.repository.update(entry)
        return entry
    
    async def delete_entry(self, entry_id: UUID) -> None:
        if not entry_id:
            raise ValueError("Entry ID is required")
        
        entryInDb = await self.repository.find_by_id(entry_id)

        if not entryInDb:
            raise ValueError("Entry not found")

        await self.repository.delete(entry_id)