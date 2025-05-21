from typing import AsyncGenerator, List
from uuid import UUID
from app.application.dto.chat_context import ChatContext
from app.application.dto.chat_item import ChatItem
from app.application.dto.question_answer import QuestionAnswer
from app.application.port.inbound.answer_use_case import AnswerUseCase
from app.application.port.inbound.chat_message_use_case import ChatMessageUseCase
from app.application.port.inbound.chat_session_use_case import ChatSessionUseCase
from app.application.port.inbound.journal_use_case import JournalUseCase
from app.application.port.inbound.questionnaire_use_case import QuestionnaireUseCase
from app.application.port.outbound.llm_provider import LLMProvider

class ChatOrchestratorService:
    def __init__(
        self, 
        chat_session_uc: ChatSessionUseCase,
        chat_message_uc: ChatMessageUseCase,
        questionnaire_uc: QuestionnaireUseCase,
        answer_uc: AnswerUseCase,
        journal_uc: JournalUseCase,
        llm_provider: LLMProvider,
    ):
        self.chat_session_uc = chat_session_uc
        self.chat_message_uc = chat_message_uc
        self.questionnaire_uc = questionnaire_uc
        self.answer_uc = answer_uc
        self.journal_uc = journal_uc
        self.llm_provider = llm_provider
        

    async def execute(
        self,
        session_id: UUID | None,
        user_id: str,
        message: str
    ) -> AsyncGenerator[dict, None]:
        title = None
        is_new_session = False
        session = None

        # 1. Verificar o crear sesión
        if session_id:
            session = await self.chat_session_uc.get_by_id(session_id)
        if not session:
            session_created = await self.chat_session_uc.create(user_id, title="Nuevo chat")
            session_id = session_created.id
            is_new_session = True

            # 1.1 Generar título
            #title_prompt = f"Genera un título breve y descriptivo para esta conversación: '{message}'"
            #title_context = ChatContext(
            #    questionnaire=[], journal_entries=[], chat_history=[], current_message=title_prompt
            #)
            #title = ""
            #async for chunk in self.llm_provider.stream_chat(title_context):
            #    title += chunk
            #title = title.strip().strip('"')[:100]
#
            #await self.chat_session_uc.update_title(session_id, title)

        # Emitir session_id y título si fue una nueva sesión
        if is_new_session:
            yield {
                "session_id": str(session_id),
                "title": "Nuevo titulo del chat"
            }

        # 2. Guardar mensaje del usuario
        await self.chat_message_uc.create(session_id, sender='user', message=message)

        # 3. Obtener contexto
        questionnaires = await self.questionnaire_uc.get_all()
        answers = await self.answer_uc.get_by_user(user_id)
        journals = await self.journal_uc.get_all_by_user(user_id)
        chats = await self.chat_message_uc.get_by_session(session_id)

        # 4. Preparar data
        question_answers: List[QuestionAnswer] = []
        for questionnaire in questionnaires:
            for question in questionnaire.questions:
                answer = next((a for a in answers if a.question_id == question.id), None)
                question_answers.append(QuestionAnswer(
                    question_id=question.id,
                    questionnaire=questionnaire.title,
                    question=question.prompt,
                    answer=answer.content if answer else ''
                ))

        journal_texts: List[str] = [entry.content for entry in journals]
        chat_items: List[ChatItem] = [
            ChatItem(sender=chat.sender, content=chat.content, send_at=chat.send_at)
            for chat in chats
        ]

        context = ChatContext(
            questionnaire=question_answers,
            journal_entries=journal_texts,
            chat_history=chat_items,
            current_message=message
        )

        # 6. Llamar al proveedor LLM
        full_response = ""
        async for chunk in self.llm_provider.stream_chat(context):
            full_response += chunk
            yield {"data": chunk}  # chunk del LLM

        # 7. Guardar respuesta completa
        await self.chat_message_uc.create(session_id, sender='ai', message=full_response)







