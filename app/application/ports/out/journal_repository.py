from typing import Protocol

from app.domain.models.journal_entry import JournalEntry


class JournalRepository(Protocol):
    def save(self, journal_entry:JournalEntry):
        pass

    def delete_by_id(self, id:str):
        pass

    def find_all_by_user_id(self, user_id:str):
        pass