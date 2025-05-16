from dataclasses import dataclass
import datetime

@dataclass
class Answer:
    id: str
    user_id: str
    question_id: str
    answer_text: str
    created_at: datetime
    updated_at: datetime