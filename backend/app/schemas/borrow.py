from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.borrow import BorrowStatus

class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

    model_config = {"from_attributes": True}

class BookResponse(BaseModel):
    id: int
    title: str
    author: Optional[str] = None

    model_config = {"from_attributes": True}

class BorrowCreate(BaseModel):
    user_id: int
    book_id: int
    days: Optional[int] = 14

class BorrowResponse(BaseModel):
    id: int
    user: UserResponse
    book: BookResponse
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    status: BorrowStatus
    extension_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class BorrowStatsResponse(BaseModel):
    totalBorrows: int
    activeBorrows: int
    returnedBorrows: int
    overdueBorrows: int
