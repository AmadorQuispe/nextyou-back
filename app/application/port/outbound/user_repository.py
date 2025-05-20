
from typing import Protocol
from uuid import UUID


from app.domain.user import User

class UserRepository(Protocol):
    def save(self, user: User) -> User:
        ...

    def find_by_id(self, id: UUID) -> User | None:
        ...
    
    def find_by_external_id(self, external_id: str) -> User | None:
        ...

    