
# Modified by GPT: CRUD class for Book based on your schema
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional, Dict
from app.models.book import Book
from app.models.book_review import BookReview
from app.models.user_rating import UserRating
from app.schemas.book_review import BookReviewOut
from app.api.book_review import get_user_from_api

class RateBookCRUD:

    @staticmethod
    async def rate_book(db: AsyncSession, book_id: int, rating: float, user_id: str) -> Optional[Book]:
  
        result = await db.execute(select(Book).filter(Book.book_id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return None

        # 2️⃣ Try to find existing rating
        result = await db.execute(
            select(UserRating).filter(
                UserRating.user_id == user_id,
                UserRating.book_id == book_id
            )
        )
        existing_rating = result.scalar_one_or_none()
        print(existing_rating)

        if existing_rating:
            # Update old rating
            raise HTTPException(status_code=400, detail="User has already rated this book.")
        else:
            # Create new rating
            new_rating = UserRating(user_id=user_id, book_id=book_id, rating=rating)
            db.add(new_rating)

        await db.commit()

        # 3️⃣ Recalculate average rating for this book
        avg_result = await db.execute(
            select(func.avg(UserRating.rating))
            .filter(UserRating.book_id == book_id)
        )
        avg_rating = float(avg_result.scalar() or 0)

        # 4️⃣ Update book table
        book.book_rating = avg_rating
        await db.commit()
        await db.refresh(book)

        return book
    

    @staticmethod
    async def get_rating_breakdown(db: AsyncSession, book_id: int) -> Dict:
    # Total number of ratings
        total_result = await db.execute(
            select(func.count(UserRating.rating_id)).where(UserRating.book_id == book_id)
        )
        total = total_result.scalar() or 0

        # Average rating
        avg_result = await db.execute(
            select(func.avg(UserRating.rating)).where(UserRating.book_id == book_id)
        )
        overall = float(avg_result.scalar() or 0)

        # Breakdown 1-5 stars
        breakdown = {}
        for star in range(1, 6):
            count_result = await db.execute(
                select(func.count(UserRating.rating_id))
                .where(UserRating.book_id == book_id, UserRating.rating == star)
            )
            count = count_result.scalar() or 0
            breakdown[star] = int((count / total) * 100) if total > 0 else 0

        # All reviews for this book
        reviews_result = await db.execute(
            select(BookReview).where(BookReview.book_id == book_id)
        )
        reviews = reviews_result.scalars().all()

        # ✅ Convert ORM → dict via Pydantic
        enriched_reviews = []
        for r in reviews:
            user_res = await get_user_from_api(r.user_id, db)
            r.username = user_res.user_name if user_res else "Unknown"
            # serialize with Pydantic
            enriched_reviews.append(BookReviewOut.model_validate(r, from_attributes=True).model_dump())
        return {
            "book_id": book_id,
            "total": total,
            "overall": round(overall, 1),
            "breakdown": breakdown,
            "reviews": enriched_reviews
        }