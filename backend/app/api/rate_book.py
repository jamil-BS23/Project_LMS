
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.book import BookCRUD
from app.database import get_db
from app.schemas.book import BookDetail,RateBook
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.patch("/rate/{book_id}", response_model=BookDetail)
async def rate_book(
    payload: RateBook,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await BookCRUD.rate_book(
        db,
        book_id=payload.book_id,
        rating=payload.book_rating,
        user_id=current_user.user_id
    )

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book