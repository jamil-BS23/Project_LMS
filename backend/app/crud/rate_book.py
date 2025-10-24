
# Modified by GPT: CRUD class for Book based on your schema
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional
from app.models.book import Book
from app.models.user_rating import UserRating

class RateBook:


    async def rate_book(self, db: AsyncSession, book_id: int, rating: float, user_id: str) -> Optional[Book]:
  
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