
from uuid import UUID
from pydantic import BaseModel


class UserSessionResponse(BaseModel):
    user_id: UUID
    answers_count: int