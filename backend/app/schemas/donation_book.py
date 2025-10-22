from pydantic import BaseModel, HttpUrl
from typing import Optional

class DonationBookPublic(BaseModel):
    book_title: str
    book_author: str
    book_category: str
    book_description: Optional[str] = None
    BS_email: str
    BS_ID: str
    book_image: Optional[HttpUrl] = None
    book_audio: Optional[HttpUrl] = None
    book_pdf: Optional[HttpUrl] = None
    available_copies: int = 1

class DonationBookCreate(DonationBookPublic):
    pass

class DonationBookResponse(DonationBookPublic):
    donation_book_id: int
    donation_status: str

    class Config:
        orm_mode = True
class DonationStatusUpdate(BaseModel):
    status: str

    class Config:
        orm_mode = True 