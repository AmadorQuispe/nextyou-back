from app.config.settings import settings
from app.infrastructure.db.postgres import Postgres


settings = settings()

class Infrastructure:
    db: Postgres = Postgres(
        dsn=f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
   

    @classmethod
    async def db_startup(cls):
        await cls.db.connect()
    
    @classmethod
    async def db_shutdown(cls):
        await cls.db.disconnect()

    @classmethod
    def openai_api_key(cls):
        return settings.openai_api_key
