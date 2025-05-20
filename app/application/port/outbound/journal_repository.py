from typing import List, Protocol
from uuid import UUID

from app.domain.journal_entry import JournalEntry


class JournalRepository(Protocol):
    def find_by_user(self, user_id: UUID) -> List[JournalEntry]:
        ...

    def find_by_id(self, entry_id: UUID) -> JournalEntry | None:
        ...

    def create(self, entry: JournalEntry) -> None:
        ...

    def update(self, entry: JournalEntry) -> None:
        ...

    def delete(self, entry_id: UUID) -> None:
        ...