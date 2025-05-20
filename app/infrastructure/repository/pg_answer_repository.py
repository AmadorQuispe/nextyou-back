from typing import List
from uuid import UUID
from app.domain.answer import Answer
from app.application.port.outbound.answer_repository import AnswerRepository
from app.infrastructure.db.postgres import Postgres


class PostgresAnswerRepository(AnswerRepository):
    def __init__(self, db: Postgres):
        self.db = db

    async def save(self, answer: Answer) -> Answer:
        query = """
            INSERT INTO answers (user_id, question_id, content, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id, question_id) DO UPDATE SET content = $3, updated_at = $5
        """
        await self.db.execute(query, answer.user_id, answer.question_id, answer.content)
        return answer
    
    async def save_batch(self, answers: List[Answer]) -> List[Answer]:
        if not answers:
            return []

        placeholders = []
        values = []

        for i, a in enumerate(answers):
            offset = i * 6
            placeholders.append(f"(${offset + 1}, ${offset + 2}, ${offset + 3}, ${offset + 4}, ${offset + 5}, ${offset + 6})")
            values.extend([
                a.id,
                a.user_id,
                a.question_id,
                a.content,
                a.created_at,
                a.updated_at
            ])

        query = f"""
            INSERT INTO answers (id, user_id, question_id, content, created_at, updated_at)
            VALUES {', '.join(placeholders)}
            ON CONFLICT (user_id, question_id) DO UPDATE 
            SET content = EXCLUDED.content,
                updated_at = EXCLUDED.updated_at
        """

        await self.db.execute(query, *values)
        return answers
    
    async def find_by_id(self, answer_id: UUID) -> Answer | None:
        query = """
            SELECT id, user_id, question_id, content, created_at, updated_at
            FROM answers
            WHERE id = $1
        """
        row = await self.db.fetch(query, answer_id)
        if not row:
            return None
        return Answer(**dict(row))

    async def find_all_by_user_id(self, user_id: UUID) -> List[Answer]:
        query = """
            SELECT id, user_id, question_id, content, created_at, updated_at
            FROM answers
            WHERE user_id = $1
        """
        rows = await self.db.fetch(query, user_id)
        return [Answer(**dict(row)) for row in rows]
    
    async def count_by_user(self, user_id: UUID) -> int:
        query = """
            SELECT COUNT(*) FROM answers WHERE user_id = $1
        """
        row = await self.db.fetchrow(query, user_id)
        return row[0]