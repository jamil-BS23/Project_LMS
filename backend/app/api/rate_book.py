
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.book import BookCRUD
from app.database import get_db
from app.schemas.book import BookDetail,RateBook
from app.core.security import get_current_user
from app.models.user import User
from typing import Dict

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


@router.get("/{book_id}/rating-breakdown")
async def get_rating_breakdown(book_id: int, db: AsyncSession = Depends(get_db)) -> Dict:
    try:
        stats = await RateBookCRUD.get_rating_breakdown(db, book_id)
        if not stats or stats.get("total", 0) == 0:
            return {
                "total": 0,
                "average": 0.0,
                "counts": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0},
                "reviews": []
            }
        return stats
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch rating breakdown: {str(e)}")
