
from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel


class AnswerCreate(BaseModel):
    question_id: UUID
    content: str

class AnswerCreateBatch(BaseModel):
    answers: List[AnswerCreate]

class AnswerUpdate(BaseModel):
    answer_id: UUID
    content: str

class AnswerResponse(BaseModel):
    id: UUID
    question_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime | None = None