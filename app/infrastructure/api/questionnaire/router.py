from fastapi import APIRouter, HTTPException, Request
from app.infrastructure.container import Container



router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])
container = Container()

@router.get("", response_model=list)
async def get_all(req: Request, with_answer: bool = False):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id found in session")
    if with_answer:
        use_case_questionnaire = container.use_case_questionnaire
        return await use_case_questionnaire.get_all_with_question_and_answer(user_id=user_id)
    use_case_questionnaire = container.use_case_questionnaire
    return await use_case_questionnaire.get_all()