from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime, timedelta

class BorrowBase(BaseModel):
    user_id: int
    book_id: int
    borrow_date: datetime
    status: str = "pending"

    @property
    def due_date(self) -> date:
        return (self.borrow_date + timedelta(days=10)).date()


class BorrowCreate(BorrowBase):
    pass

class BorrowUpdate(BaseModel):
    status: Optional[str] = None
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: date
    return_date: Optional[datetime] = None
    status: str

    class Config:
        orm_mode = True

class BorrowLimit(BaseModel):
    user_id: int
    borrowed_count: int
    max_limit: int = 5

class BorrowListResponse(BaseModel):
    borrows: List[BorrowResponse]
