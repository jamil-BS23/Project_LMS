from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.borrow import BorrowCreate, BorrowResponse, BorrowUpdate
import app.crud.borrow as crud_borrow 
from app.database import get_db

router = APIRouter(prefix="/borrows", tags=["borrows"])

@router.post("/", response_model=BorrowResponse)
async def create_borrow(borrow: BorrowCreate, db: AsyncSession = Depends(get_db)):
    return await crud_borrow.create_borrow(db, borrow)

@router.get("/", response_model=List[BorrowResponse])
async def list_borrows(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_borrow.get_borrows(db, skip=skip, limit=limit)

@router.get("/{borrow_id}", response_model=BorrowResponse)
async def get_borrow(borrow_id: int, db: AsyncSession = Depends(get_db)):
    db_borrow = await crud_borrow.get_borrow(db, borrow_id)
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return db_borrow

@router.put("/{borrow_id}", response_model=BorrowResponse)
async def update_borrow(borrow_id: int, borrow_update: BorrowUpdate, db: AsyncSession = Depends(get_db)):
    db_borrow = await crud_borrow.update_borrow(db, borrow_id, borrow_update)
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return db_borrow
