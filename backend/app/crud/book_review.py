from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book_review import BookReview
from app.models.book import Book


class BookReviewCRUD:
    @staticmethod
    async def create_review(
        db: AsyncSession, user_id: str, book_id: int, review_text: str
    ):
        review = BookReview(user_id=user_id, book_id=book_id, review_text=review_text)
        db.add(review)

        await db.commit()
        await db.refresh(review)
        return review

    @staticmethod
    async def get_reviews(db: AsyncSession, book_id: int):
        result = await db.execute(
            select(BookReview).where(BookReview.book_id == book_id)
        )
        return result.scalars().all()
