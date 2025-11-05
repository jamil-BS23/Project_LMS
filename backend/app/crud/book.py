# Modified by GPT: CRUD class for Book based on your schema
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc, func
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from datetime import datetime
from typing import Optional, List
from app.models.book import Book
from app.models.user_rating import UserRating
from app.schemas.book import BookCreate, BookUpdate


class BookCRUD:
    """CRUD operations for Book"""

    def __init__(self):
        pass

    async def get_all(
        self,
        db: AsyncSession,
        search: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Book]:
        query = select(Book)

        if search:
            like_pattern = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    Book.book_title.ilike(like_pattern),
                    Book.book_author.ilike(like_pattern),
                    Book.book_description.ilike(like_pattern),
                    Book.book_category.ilike(like_pattern),
                )
            )

        if category:
            query = query.filter(Book.book_category == category)

        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def count_books(db: AsyncSession) -> int:
        """
        Return total number of books in the library.
        """
        result = await db.execute(select(func.count()).select_from(Book))
        return result.scalar_one()

    async def get_by_id(self, db: AsyncSession, book_id: int) -> Optional[Book]:
        result = await db.execute(select(Book).where(Book.book_id == book_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, book_data: BookCreate) -> Book:
        new_book = Book(**book_data.dict())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book

    async def update(
        self, db: AsyncSession, book_id: int, update_data: BookUpdate
    ) -> Optional[Book]:
        book = await self.get_by_id(db, book_id)
        if not book:
            return None
        protected_fields = {"book_availabity", "featured", "book_rating"}

        for key, value in update_data.dict(exclude_unset=True).items():
            if key not in protected_fields:
                setattr(book, key, value)
        await db.commit()
        await db.refresh(book)
        return book

    async def delete(self, db: AsyncSession, book_id: int) -> bool:
        book = await self.get_by_id(db, book_id)
        if not book:
            return False
        await db.delete(book)
        await db.commit()
        return True

    async def get_featured(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[Book]:
        result = await db.execute(
            select(Book).where(Book.featured == True).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_popular(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[Book]:
        result = await db.execute(
            select(Book).order_by(desc(Book.book_rating)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_new(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[Book]:
        result = await db.execute(
            select(Book).order_by(desc(Book.created_at)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def rate_book(
        self, db: AsyncSession, book_id: int, rating: float, user_id: str
    ) -> Optional[Book]:

        result = await db.execute(select(Book).filter(Book.book_id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return None

        result = await db.execute(
            select(UserRating).filter(
                UserRating.user_id == user_id, UserRating.book_id == book_id
            )
        )
        existing_rating = result.scalar_one_or_none()
        print(existing_rating)

        if existing_rating:
            raise HTTPException(
                status_code=400, detail="User has already rated this book."
            )
        else:
            new_rating = UserRating(user_id=user_id, book_id=book_id, rating=rating)
            db.add(new_rating)

        await db.commit()

        avg_result = await db.execute(
            select(func.avg(UserRating.rating)).filter(UserRating.book_id == book_id)
        )
        avg_rating = float(avg_result.scalar() or 0)

        book.book_rating = avg_rating
        await db.commit()
        await db.refresh(book)

        return book

    async def toggle_featured(
        self, db: AsyncSession, book_id: int, featured: bool
    ) -> Optional[Book]:
        book = await self.get_by_id(db, book_id)
        if not book:
            return None
        book.featured = featured
        await db.commit()
        await db.refresh(book)
        return book
