# app/schemas/borrow.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# Input schema for creating a borrow
class BorrowCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user borrowing the book")
    book_id: int = Field(..., description="ID of the book to borrow")
    due_date: Optional[date] = Field(None, description="Optional due date for returning the book")

# Response schema for a single borrow record
class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    due_date: date
    returned_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BorrowLimit(BaseModel):
    user_id: int
    borrowed_count: int
    max_limit: int = 5 

class BorrowListResponse(BaseModel):
    borrows: List[BorrowResponse]
