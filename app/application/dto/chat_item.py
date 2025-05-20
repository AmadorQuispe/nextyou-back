from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatItem:
    sender: str
    content: str
    send_at: datetime