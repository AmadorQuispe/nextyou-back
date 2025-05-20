from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.infrastructure.api.journal.schemas import (
    JournalEntryCreate, JournalEntryUpdate, JournalEntryResponse
)
from app.application.service.journal_service import JournalService
from uuid import UUID
from typing import List
from app.infrastructure.container import Container

router = APIRouter(prefix="/journals", tags=["Journals"])
container = Container()



@router.get("", response_model=List[JournalEntryResponse])
async def get_entries_by_user(req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")
    use_case_journal = container.use_case_journal
    return await use_case_journal.get_all_by_user(user_id=user_id)

@router.post("", response_model=JournalEntryResponse)
async def create_entry(entry: JournalEntryCreate, req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")
    use_case_journal = container.use_case_journal
    return await use_case_journal.add_entry(user_id=user_id, content=entry.content)

@router.put("/{entry_id}", response_model=JournalEntryResponse)
async def update_entry(entry_id: UUID, entry: JournalEntryUpdate, req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")
    use_case_journal = container.use_case_journal
    return await use_case_journal.update_entry(entry_id=entry_id, new_content=entry.content)

@router.delete("/{entry_id}", response_model=None)
async def delete_entry(entry_id: UUID, req: Request):
    user_id = getattr(req.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id")
    use_case_journal = container.use_case_journal
    return await use_case_journal.delete_entry(entry_id=entry_id)
