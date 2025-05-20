


from uuid import UUID
from pydantic import BaseModel


class ChatMessageUser(BaseModel):
    message: str
    session_id: UUID | None = None