
from app.application.port.inbound.questionnaire_use_case import QuestionnaireUseCase
from app.application.port.outbound.question_repository import QuestionRepository
from app.application.port.outbound.questionnaire_repository import QuestionnaireRepository
from app.application.service.questionnaire_service import QuestionnaireService
from app.application.port.outbound.journal_repository import JournalRepository
from app.application.port.inbound.journal_use_case import JournalUseCase

from app.infrastructure.infrastructure import Infrastructure
from app.infrastructure.repository.pg_journal_repository import PostgresJournalRepository
from app.application.service.journal_service import JournalService
from app.infrastructure.repository.pg_question_repository import PostgresQuestionRepository
from app.infrastructure.repository.pg_questionnaire_repository import PostgresQuestionnaireRepository

from app.application.port.inbound.answer_use_case import AnswerUseCase
from app.application.port.outbound.answer_repository import AnswerRepository
from app.application.service.answer_service import AnswerService
from app.infrastructure.repository.pg_answer_repository import PostgresAnswerRepository

from app.application.port.inbound.user_use_case import UserUseCase
from app.application.port.outbound.user_repository import UserRepository
from app.application.service.user_service import UserService
from app.infrastructure.repository.pg_user_repository import PostgresUserRepository

from app.application.port.inbound.chat_session_use_case import ChatSessionUseCase
from app.application.port.outbound.chat_session_repository import ChatSessionRepository
from app.application.service.chat_session_service import ChatSessionService
from app.infrastructure.repository.pg_chat_session_repository import PostgresChatSessionRepository

from app.application.port.inbound.chat_message_use_case import ChatMessageUseCase
from app.application.port.outbound.chat_message_repository import ChatMessageRepository
from app.application.service.chat_message_service import ChatMessageService
from app.infrastructure.repository.pg_chat_message_repository import PostgresChatMessageRepository

from app.application.port.outbound.llm_provider import LLMProvider
from app.infrastructure.provider.openai_llm_provider import OpenaiLLMProvider

from app.application.port.inbound.chat_orchestrator_use_case import ChatOrchestratorUseCase
from app.application.service.chat_orchestrator_service import ChatOrchestratorService



class Container:
    @property
    def use_case_user(self) -> UserUseCase:
        repo_user: UserRepository = PostgresUserRepository(Infrastructure.db)
        return UserService(repo_user)

    @property
    def use_case_journal(self) -> JournalUseCase:
        repo: JournalRepository = PostgresJournalRepository(Infrastructure.db)
        return JournalService(repo)
    
    @property
    def use_case_questionnaire(self) -> QuestionnaireUseCase:
        repo_questionnaire: QuestionnaireRepository = PostgresQuestionnaireRepository(Infrastructure.db)
        repo_question: QuestionRepository = PostgresQuestionRepository(Infrastructure.db)
        repo_answer: AnswerRepository = PostgresAnswerRepository(Infrastructure.db)
        return QuestionnaireService(repo_questionnaire, repo_question,  repo_answer)
    
    @property
    def use_case_answer(self) -> AnswerUseCase:
        repo_answer: AnswerRepository = PostgresAnswerRepository(Infrastructure.db)
        return AnswerService(repo_answer)
    
    @property
    def use_case_chat_session(self) -> ChatSessionUseCase:
        repo: ChatSessionRepository = PostgresChatSessionRepository(Infrastructure.db)
        return ChatSessionService(repo, self.use_case_chat_message)
    
    @property
    def use_case_chat_message(self) -> ChatMessageUseCase:
        repo: ChatMessageRepository = PostgresChatMessageRepository(Infrastructure.db)
        return ChatMessageService(repo)
    
    @property
    def llm_provider(self) -> LLMProvider:
        
        return OpenaiLLMProvider(Infrastructure.openai_api_key())
    
    @property
    def chat_orchestrator(self) -> ChatOrchestratorUseCase:
        return ChatOrchestratorService(
            self.use_case_chat_session,
            self.use_case_chat_message,
            self.use_case_questionnaire,
            self.use_case_answer,
            self.use_case_journal,
            self.llm_provider
        )