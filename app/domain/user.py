from dataclasses import dataclass
import datetime

@dataclass
class User:
    id: str
    external_id: str
    provider: str #!TODO: enum
    created_at: datetime
    updated_at: datetime