from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.infrastructure.api.chat_session.schemas import ChatSessionRequest, ChatSessionResponse
from app.infrastructure.container import Container


router = APIRouter(prefix="/chat_sessions", tags=["Chat Sessions"])
container = Container()

@router.get("", response_model=list[ChatSessionResponse])
async def get_all(req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id found in session")
    use_case_chat_session = container.use_case_chat_session
    return await use_case_chat_session.get_all_by_user(user_id=user_id)

@router.get("/{session_id}", response_model=ChatSessionResponse)
async def get_by_id(session_id: UUID, req: Request, tree: bool = False):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id found in session")
    use_case_chat_session = container.use_case_chat_session
    return await use_case_chat_session.get_by_id(session_id=session_id, tree=tree)

@router.post("", response_model=ChatSessionResponse)
async def create(req: Request, chat_session: ChatSessionRequest):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id found in session")
    use_case_chat_session = container.use_case_chat_session
    session = await use_case_chat_session.create(user_id=user_id, title=chat_session.title)
    return session