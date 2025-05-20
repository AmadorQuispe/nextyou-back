from uuid import UUID
from app.domain.user import User
from app.application.port.outbound.user_repository import UserRepository
from app.infrastructure.db.postgres import Postgres


class PostgresUserRepository(UserRepository):
    def __init__(self, db: Postgres):
        self.db = db

    async def save(self, user: User) -> User:
        query = """
            INSERT INTO users (id, external_id, provider, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE 
            SET external_id = EXCLUDED.external_id, provider = EXCLUDED.provider, updated_at = EXCLUDED.updated_at
        """
        await self.db.execute(query, user.id, user.external_id, user.provider, user.created_at, user.updated_at)
        return user
    
    async def find_by_id(self, id: UUID) -> User | None:
        query = """
            SELECT id, external_id, provider, created_at, updated_at
            FROM users
            WHERE id = $1
        """
        row = await self.db.fetchrow(query, id)
        if not row:
            return None
        return User(**row)
    
    async def find_by_external_id(self, external_id: str) -> User | None:
        query = """
            SELECT id, external_id, provider, created_at, updated_at
            FROM users
            WHERE external_id = $1
        """
        row = await self.db.fetchrow(query, external_id)
        if not row:
            return None
        return User(**row)