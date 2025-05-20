import json
from uuid import UUID
from fastapi import APIRouter, HTTPException,  Request
from fastapi.responses import StreamingResponse
from app.infrastructure.api.chat.schemas import ChatMessageUser
from app.infrastructure.container import Container

router = APIRouter(prefix="/chat", tags=["chats"])
container = Container()

@router.post("", response_class=StreamingResponse)
@router.post("/{session_id}", response_class=StreamingResponse)
async def chat_stream(
    chat_message: ChatMessageUser, 
    req: Request,
    session_id: UUID | None = None
):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id found in session")
    stream = container.chat_orchestrator.execute(
        session_id=session_id,
        user_id=user_id,
        message=chat_message.message
    )

    async def sse_format():
        async for item in stream:
            if "session_id" in item:
                yield f"event: session_id\ndata: {item['session_id']}\n\n"
            if "title" in item:
                yield f"event: title\ndata: {item['title']}\n\n"
            if "data" in item:
                delta_data = {"c": item['data']}
                yield f"event: delta\ndata: {json.dumps(delta_data)}\n\n"


    return StreamingResponse(sse_format(), media_type="text/event-stream")
