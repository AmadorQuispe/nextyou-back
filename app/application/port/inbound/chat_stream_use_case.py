
from typing import AsyncGenerator, Protocol


class ChatStreamUseCase(Protocol):

    def stream_response(self, message: str) -> AsyncGenerator[str, None]:
        ...