from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookReviewCreate(BaseModel):
    book_id: int
    review_text: str

class BookReviewOut(BaseModel):
    review_id: int
    user_id: str
    username: Optional[str] = None
    book_id: int
    review_text: str
    created_at: datetime

    model_config = {
        "from_attributes": True 
    }
