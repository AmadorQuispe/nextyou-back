

from dataclasses import dataclass
from typing import List

from app.application.dto.chat_item import ChatItem
from app.application.dto.question_answer import QuestionAnswer


@dataclass
class ChatContext:
    questionnaire: List[QuestionAnswer]
    journal_entries: List[str]
    chat_history: List[ChatItem]
    current_message: str
