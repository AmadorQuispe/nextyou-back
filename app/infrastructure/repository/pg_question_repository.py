from typing import List
from app.domain.question import Question
from app.application.port.outbound.question_repository import QuestionRepository
from app.infrastructure.db.postgres import Postgres
from uuid import UUID

class PostgresQuestionRepository(QuestionRepository):
    def __init__(self, db: Postgres):
        self.db = db
    
    async def find_all(self) -> List[Question]:
        try:
            query = """
                SELECT id,questionnaire_id, prompt, helper, position, created_at, updated_at
                FROM questions
            """
            rows = await self.db.fetch(query)
            return [Question(**dict(row)) for row in rows]
    
        except Exception as e:
            raise ValueError("Error fetching questions")
    
    async def find_by_id(self, id: UUID) -> Question | None:
        query = """
            SELECT id,questionnaire_id, prompt, helper, position, created_at, updated_at
            FROM questions
            WHERE id = $1
        """
        row = await self.db.fetch(query, id)
        if not row:
            return None
        return Question(**dict(row))
