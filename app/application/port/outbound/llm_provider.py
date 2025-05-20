
from typing import AsyncGenerator, Protocol


class LLMProvider(Protocol):
    def stream_chat(self, prompt: str) -> AsyncGenerator[str, None]:
        ...