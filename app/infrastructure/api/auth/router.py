from fastapi import APIRouter, HTTPException, Request, Response

from app.infrastructure.api.auth.schemas import UserSessionResponse
from app.infrastructure.clerk.verify_token import verify_token
from app.infrastructure.container import Container


router = APIRouter(prefix="/auth", tags=["Auth"])
container = Container()

@router.post("/session", response_model=UserSessionResponse)
async def create_session(request: Request, response: Response):
    if(request.headers.get("Authorization") is None):
        raise HTTPException(status_code=401, detail="No token provided")
    
    token = request.headers.get("Authorization").split(" ")[1]

    payload = await verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id_external = payload["sub"]
    answers_count = 0
    user_in_db = await container.use_case_user.find_by_external_id(user_id_external)
    user_id = user_in_db.id if user_in_db else None
    if not user_id:                
        user_created = await container.use_case_user.create(user_id_external, "clerk")
        user_id = user_created.id
    else:
        answers_count = await container.use_case_answer.count_by_user(user_id)

    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60 * 24 * 7
    )

    return UserSessionResponse(user_id=user_id, answers_count=answers_count)