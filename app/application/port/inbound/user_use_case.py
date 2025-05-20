

from typing import Protocol
from uuid import UUID
from app.domain.user import User

class UserUseCase(Protocol):
    def create(self, external_id: str, provider: str) -> User:
        ...
        
    def update(self, user_id: str, external_id: str, provider: str) -> User:
        ...

    def find_by_id(self, user_id: UUID) -> User | None:
        ...

    def find_by_external_id(self, external_id: str) -> User | None:
        ...
