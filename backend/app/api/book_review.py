from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import traceback

from app.crud.book_review import BookReviewCRUD
from app.schemas.book_review import BookReviewCreate, BookReviewOut
from app.dependencies import get_current_user
from app.database import get_db
from app.crud.user import UserCRUD 

router = APIRouter()


async def get_user_from_api(user_id: int, db: AsyncSession):
    """
    Helper function to fetch user details by ID.
    """
    try:
        user = await UserCRUD.get_user(db, user_id)
        return user
    except Exception:
        traceback.print_exc()
        return None


@router.post("/{book_id}", response_model=BookReviewOut, status_code=status.HTTP_201_CREATED)
async def add_review(
    book_id: int,
    review: BookReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Add a new review for a book.
    """
    try:
        new_review = await BookReviewCRUD.create_review(
            db, current_user.user_id, book_id, review.review_text
        )
        return new_review
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add review: {str(e)}"
        )



@router.get("/{book_id}", response_model=List[BookReviewOut])
async def get_book_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get all reviews for a specific book.
    """
    try:
        reviews = await BookReviewCRUD.get_reviews(db, book_id)
        if not reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No reviews found for this book."
            )

        for r in reviews:
            user_res = await get_user_from_api(r.user_id, db)
            r.username = user_res.user_name if user_res else "Unknown"

        return reviews
    except Exception as e:
<<<<<<< HEAD
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch reviews: {str(e)}"
        )
=======
        import traceback
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")

>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
