from pydentic import BaseModel
from typing import Optional
from pydantic import Field, HttpUrl
from datetime import datetime

class BookDetail(BaseModel):
    book_id: int
    book_title: str
    book_category: str
    book_author: str
    book_description: Optional[str] = None
    available_copies: int
    created_at: datetime
    book_availabity: bool
    featured: bool
    book_rating: float
    book_image: Optional[str] = None
    book_audio: Optional[str] = None
    book_pdf: Optional[str] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class BookDetail2(BaseModel):
    book_id: int
    book_title: str
    book_author: str
    book_category_id: int
    category_title: str
    book_rating: float
    book_photo: Optional[HttpUrl]
    book_pdf: Optional[HttpUrl]
    book_audio: Optional[HttpUrl]
    book_details: Optional[str]
    book_availability: bool = Field(..., alias="book_availability")
    book_count: int
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BookCreate(BaseModel):
    book_title: str
    book_category: str
    book_author: str
    book_description: Optional[str] = None
    available_copies: int = 0
    book_availabity: bool = True
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    book_rating: float = 0.0
    book_image: Optional[str] = None
    book_audio: Optional[str] = None
    book_pdf: Optional[str] = None

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    book_title: Optional[str] = None
    book_category: Optional[str] = None
    book_author: Optional[str] = None
    book_description: Optional[str] = None
    available_copies: Optional[int] = None
    book_availabity: Optional[bool] = None
    featured: Optional[bool] = None
    book_rating: Optional[float] = None
    book_image: Optional[str] = None
    book_audio: Optional[str] = None
    book_pdf: Optional[str] = None

    class Config:
        orm_mode = True

class RateBook(BaseModel):
    book_id: int
    book_rating: float

    class Config:
        orm_mode = True

class UpoadateFeatures(BaseModel):
    featured: bool

    class Config:
        orm_mode = True