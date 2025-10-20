from pydantic import BaseModel, httpUrl
from typing import Optional

class DonationBookBase(BaseModel):
    book_title: str
    book_author: str
    book_category: str
    book_description: Optional[str] = None
    BS_email: str
    BS_ID: str
    book_image: Optional[httpUrl] = None
    book_audio: Optional[httpUrl] = None
    book_pdf: Optional[httpUrl] = None
    available_copies: int = 1

class DonationBookCreate(DonationBookBase):
    pass

class DonationBookResponse(DonationBookBase):
    donation_book_id: int
    donation_status: str

    class Config:
        orm_mode = True