from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class User:
    id: UUID
    external_id: str
    provider: str #!TODO: enum
    created_at: datetime
    updated_at: datetime | None