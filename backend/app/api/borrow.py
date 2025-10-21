from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.crud import borrow as borrow_crud
from app.schemas import borrow as borrow_schema

router = APIRouter(prefix="/borrow", tags=["Borrow & Return"])

@router.post("/create", response_model=borrow_schema.BorrowResponse)
async def create_borrow(
    request: borrow_schema.BorrowCreate,
    db: AsyncSession = Depends(get_db)
):
    borrow = await borrow_crud.create_borrow(db, request, request.user_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Book already borrowed or unavailable")
    return borrow

@router.put("/return", response_model=borrow_schema.BorrowResponse)
async def return_book(
    user_id: int = Query(...),
    book_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    borrow = await borrow_crud.return_book(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Book not borrowed or already returned")
    return borrow

@router.put("/extend_due_date", response_model=borrow_schema.BorrowResponse)
async def extend_due_date(
    user_id: int = Query(...),
    book_id: int = Query(...),
    extend_days: Optional[int] = Query(7),
    db: AsyncSession = Depends(get_db)
):
    borrow = await borrow_crud.extend_due_date(db, user_id, book_id, extend_days)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot extend due date")
    return borrow

@router.get("/user/{user_id}", response_model=List[borrow_schema.BorrowResponse])
async def get_user_borrows(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await borrow_crud.get_user_borrows(db, user_id)

@router.get("/overdue", response_model=List[borrow_schema.BorrowResponse])
async def get_overdue_borrows(
    db: AsyncSession = Depends(get_db)
):
    return await borrow_crud.get_overdue_borrows(db)
