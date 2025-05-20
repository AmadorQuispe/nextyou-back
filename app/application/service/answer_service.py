import datetime as dt
from typing import List
import uuid
from app.application.dto.answer_input import AnswerInput
from app.application.port.outbound.answer_repository import AnswerRepository
from app.domain.answer import Answer


class AnswerService:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    async def create(self, user_id: str, question_id: str, content: str) -> Answer:
        answer = Answer(
            id=uuid.uuid4(),
            user_id=user_id, 
            question_id=question_id, 
            content=content,
            created_at=dt.datetime.now(tz=dt.timezone.utc)
        )
        return await self.answer_repository.save(answer)
    
    async def create_batch(self, user_id: str, answers: list[AnswerInput]) -> list[Answer]:
        answers_to_save: list[Answer] = []
        for answer in answers:
            new_answer = Answer(
                id=uuid.uuid4(),
                user_id=user_id,
                question_id=answer.question_id,
                content=answer.content,
                created_at=dt.datetime.now(tz=dt.timezone.utc),
                updated_at=dt.datetime.now(tz=dt.timezone.utc)
            )
            answers_to_save.append(new_answer)
        return await self.answer_repository.save_batch(answers_to_save)

    async def update(self, user_id: str, answer_id: str, content: str) -> Answer:
        answer_in_db = await self.answer_repository.find_by_id(answer_id)
        if not answer_in_db:
            raise ValueError(f"Answer with id {answer_id} not found")
        if(answer_in_db.user_id != user_id):
            raise ValueError(f"User {user_id} is not authorized to update answer {answer_id}")
        
        answer = Answer(
            id=answer_id,
            user_id=user_id,
            question_id=answer_id,
            content=content,
            created_at=answer_in_db.created_at,
            updated_at=dt.datetime.now(tz=dt.timezone.utc)
        )
        return await self.answer_repository.save(answer)
    
    async def get_by_user(self, user_id: str) -> List[Answer]:
        return await self.answer_repository.find_all_by_user_id(user_id)
    
    async def count_by_user(self, user_id: uuid.UUID) -> int:
        return await self.answer_repository.count_by_user(user_id)