from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.infrastructure import Infrastructure
from app.infrastructure.middleware.clerk_auth_middleware import ClerkAuthMiddleware
from app.infrastructure.api.journal.router import router as journal_router
from app.infrastructure.api.auth.router import router as auth_router
from app.infrastructure.api.questionnaire.router import router as questionnaire_router
from app.infrastructure.api.answer.router import router as answer_router
from app.infrastructure.api.chat.router import router as chat_router
from app.infrastructure.api.chat_session.router import router as chat_session_router




origins = [
    "http://localhost:5173",  # frontend local con Vite
    "https://nextyou.amsoft.dev"  # producción
]



@asynccontextmanager
async def lifespan(app: FastAPI):
    await Infrastructure.db_startup()
    yield
    await Infrastructure.db_shutdown()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ClerkAuthMiddleware, protected_paths=["/journals", "/answers", "/chat", "/chat_sessions", "/questionnaires"])

app.include_router(journal_router)
app.include_router(auth_router)
app.include_router(questionnaire_router)
app.include_router(answer_router)
app.include_router(chat_session_router)
app.include_router(chat_router)