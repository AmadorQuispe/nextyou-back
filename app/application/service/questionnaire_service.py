from typing import List
from uuid import UUID
from app.application.dto.question_with_answer import QuestionWithAnswer
from app.application.dto.questionnaire_with_answer import QuestionnaireWithQuestionsAndAnswers
from app.application.dto.questionnaire_with_questions import QuestionnaireWithQuestions
from app.application.port.outbound.answer_repository import AnswerRepository
from app.application.port.outbound.questionnaire_repository import QuestionnaireRepository
from app.application.port.outbound.question_repository import QuestionRepository



class QuestionnaireService:
    def __init__(
            self, 
            questionnaire_repository: QuestionnaireRepository, 
            question_repository: QuestionRepository,
            answer_repository: AnswerRepository
        ):
        self.questionnaire_repository = questionnaire_repository
        self.question_repository = question_repository
        self.answer_repository = answer_repository

    async def get_all(self) -> List[QuestionnaireWithQuestions]:
        questionnaires = await self.questionnaire_repository.find_all()
        questions = await self.question_repository.find_all()

        with_questions = []
        for questionnaire in questionnaires:
            with_questions.append(QuestionnaireWithQuestions(
                id=questionnaire.id,
                title=questionnaire.title,
                description=questionnaire.description,
                position=questionnaire.position,
                questions=[question for question in questions if question.questionnaire_id == questionnaire.id]
            ))

        return with_questions
    
    async def get_all_with_question_and_answer(self, user_id: UUID) -> List[QuestionnaireWithQuestionsAndAnswers]:
        questionnaires = await self.questionnaire_repository.find_all()
        questions = await self.question_repository.find_all()
        answers = await self.answer_repository.find_all_by_user_id(user_id)

        combined: list[QuestionnaireWithQuestionsAndAnswers] = []
        for questionnaire in questionnaires:
            with_questions = []
            for question in questions:
                if question.questionnaire_id == questionnaire.id:
                    with_questions.append(QuestionWithAnswer(
                        id=question.id,
                        questionnaire_id=questionnaire.id,
                        prompt=question.prompt,
                        helper=question.helper,
                        position=question.position,
                        answer=next((a for a in answers if a.question_id == question.id), None)
                    ))
            combined.append(QuestionnaireWithQuestionsAndAnswers(
                id=questionnaire.id,
                title=questionnaire.title,
                description=questionnaire.description,
                position=questionnaire.position,
                questions=with_questions
            ))

        return combined