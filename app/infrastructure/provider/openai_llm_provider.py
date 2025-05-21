from typing import AsyncGenerator
from openai import AsyncOpenAI
from app.application.port.outbound.llm_provider import LLMProvider
from app.application.dto.chat_context import ChatContext

class OpenaiLLMProvider:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        self.model = "llama-3.3-70b-versatile"

    async def stream_chat(self, context: ChatContext) -> AsyncGenerator[str, None]:        
        prompt = self._build_messages(context)
        

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            temperature=0.7,
            stream=True
        )

        async for chunk in response:
            delta = chunk.choices[0].delta.content if chunk.choices[0].delta else ""
            if delta:
                yield delta

    def _build_messages(self, context: ChatContext) -> list[dict]:
        messages = []

        # System context message
        messages.append({
            "role": "system",
            "content": (
                "Eres una versión sabia del 'yo del futuro'. Tus respuestas deben ser reflexivas, empáticas, "
                "y basadas en el conocimiento previo del usuario: cuestionarios, entradas de diario, y conversación previa."
            )
        })

        # Incorporar contexto del usuario
        if context.questionnaire:
            questionnaire_summary = "\n".join([
                f"[{qa.questionnaire}] {qa.question}: {qa.answer}"
                for qa in context.questionnaire if qa.answer
            ])
            messages.append({
                "role": "system",
                "content": f"Información personal del usuario:\n{questionnaire_summary}"
            })

        if context.journal_entries:
            journal_summary = "\n".join(f"- {entry}" for entry in context.journal_entries)
            messages.append({
                "role": "system",
                "content": f"Entradas de diario recientes del usuario:\n{journal_summary}"
            })

        # Historial de conversación
        for item in context.chat_history:
            messages.append({
                "role": "user" if item.sender == "user" else "assistant",
                "content": item.content
            })

        # Último mensaje actual
        messages.append({
            "role": "user",
            "content": context.current_message
        })

        return messages
