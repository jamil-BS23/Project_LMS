from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.user import UserCRUD
from app.database import get_db
from app.crud.book_review import BookReviewCRUD
from app.schemas.book_review import BookReviewCreate, BookReviewOut
from app.dependencies import get_current_user  # Ensure you have this for authentication

router = APIRouter()





@router.post("/{book_id}", response_model=BookReviewOut)
async def add_review(
    book_id: int,
    review: BookReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await BookReviewCRUD.create_review(db, current_user.user_id, book_id, review.review_text)



@router.get("/{book_id}", response_model=List[BookReviewOut])
async def get_book_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    """
        Get all reviews for a specific book.
    """
    try:
        reviews = await BookReviewCRUD.get_reviews(db, book_id)
        if not reviews:
            return []
        for r in reviews:
            user_res = await get_user_from_api(r.user_id, db)
            r.username = user_res.user_name if user_res else "Unknown"
        
        return reviews
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")
    

async def get_user_from_api(user_id: str, db: AsyncSession):
    user = await UserCRUD.get_user_by_id(db, user_id)
    if not user:
        return None
    return user