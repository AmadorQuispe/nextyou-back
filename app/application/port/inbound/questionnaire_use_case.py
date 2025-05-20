from typing import Protocol
from uuid import UUID


from app.application.dto.questionnaire_with_answer import QuestionnaireWithQuestionsAndAnswers
from app.application.dto.questionnaire_with_questions import QuestionnaireWithQuestions


class QuestionnaireUseCase(Protocol):
    def get_all(self) -> list[QuestionnaireWithQuestions]:
        ...
    def get_all_with_question_and_answer(self, user_id: UUID) -> list[QuestionnaireWithQuestionsAndAnswers]:
        ...