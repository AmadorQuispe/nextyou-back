

import uuid
from app.domain.user import User
from app.application.port.outbound.user_repository import UserRepository
from app.application.port.inbound.user_use_case import UserUseCase
import datetime as dt

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, external_id, provider):
        user = User(
            id =uuid.uuid4(),
            external_id=external_id,
            provider=provider,
            created_at=dt.datetime.now(tz=dt.timezone.utc),
            updated_at=dt.datetime.now(tz=dt.timezone.utc)
        )

        return await self.repository.save(user)
    
    async def update(self, user_id, external_id, provider):
        user = User(
            id=user_id,
            external_id=external_id,
            provider=provider,
            updated_at=dt.datetime.now(tz=dt.timezone.utc)
        )
        return await self.repository.save(user)

    async def find_by_id(self, id: uuid.UUID) -> User | None:
        return await self.repository.find_by_id(id)
    
    async def find_by_external_id(self, external_id: str) -> User | None:
        return await self.repository.find_by_external_id(external_id)