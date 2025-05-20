from typing import AsyncGenerator, Protocol
from uuid import UUID

class ChatOrchestratorUseCase(Protocol):
    def execute(
            self,
            session_id:UUID | None, 
            user_id: str, 
            message: str
    ) -> AsyncGenerator[str, None]:
        ...