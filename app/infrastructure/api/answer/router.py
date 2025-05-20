from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.infrastructure.container import Container
from app.infrastructure.api.answer.schemas import AnswerCreate, AnswerUpdate, AnswerResponse

router = APIRouter(prefix="/answers", tags=["Answers"])
container = Container()

@router.get("", response_model=List[AnswerResponse])
async def get_all_by_user(req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")

    use_case_answer = container.use_case_answer
    return await use_case_answer.get_by_user(user_id=user_id)

@router.post("", response_model=AnswerResponse)
async def create_answer(answer: AnswerCreate, req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")
    use_case_answer = container.use_case_answer
    return await use_case_answer.create(user_id=user_id, question_id=answer.question_id, content=answer.content)

@router.post("/batch", response_model=List[AnswerResponse])
async def create_answers_batch(answers: List[AnswerCreate], req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")
    
    use_case_answer = container.use_case_answer
    return await use_case_answer.create_batch(user_id=user_id, answers=answers)
