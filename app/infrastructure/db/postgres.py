import asyncpg
from typing import Optional

class Postgres:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(dsn=self._dsn)

    async def disconnect(self):
        if self._pool:
            await self._pool.close()

    async def fetch(self, query: str, *args):
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)
    async def fetchrow(self, query: str, *args):
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)
