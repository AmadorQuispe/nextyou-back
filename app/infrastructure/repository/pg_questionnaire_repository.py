from typing import List
from app.domain.questionnaire import Questionnaire
from app.application.port.outbound.questionnaire_repository import QuestionnaireRepository
from app.infrastructure.db.postgres import Postgres
from uuid import UUID

class PostgresQuestionnaireRepository(QuestionnaireRepository):
    def __init__(self, db: Postgres):
        self.db = db

    async def find_all(self) -> List[Questionnaire]:
        query = """
            SELECT id, title, description, position, created_at
            FROM questionnaires
        """
        rows = await self.db.fetch(query)
        return [Questionnaire(**dict(row)) for row in rows]
    
    async def find_by_id(self, id: UUID) -> Questionnaire | None:
        query = """
            SELECT id, title, description, position, created_at
            FROM questionnaires
            WHERE id = $1
        """
        row = await self.db.fetch(query, id)
        if not row:
            return None
        return Questionnaire(**dict(row))