from typing import Protocol
from uuid import UUID
from typing import List
from app.domain.journal_entry import JournalEntry

class JournalUseCase(Protocol):
    def get_all_by_user(self, user_id: UUID) -> List[JournalEntry]:
        ...

    def add_entry(self, user_id: UUID, content: str) -> JournalEntry:
        ...
    
    def update_entry(self, entry_id: UUID, new_content: str) -> JournalEntry:
        ...

    def delete_entry(self, entry_id: UUID) -> None:
        ...
