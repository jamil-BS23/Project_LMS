# Modified by GPT: CRUD class for Book based on your schema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc
from app import models, schemas
from datetime import datetime
from typing import Optional, List
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
class BookCRUD:
    """CRUD operations for Book"""

    def __init__(self):
        pass  # no instance attributes needed; db is passed per method

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 20,
        search: Optional[str] = None, category: Optional[str] = None
    ) -> List[Book]:
        query = select(Book)
        if search:
            query = query.filter(
                or_(
                    Book.book_title.ilike(f"%{search}%"),
                    Book.book_author.ilike(f"%{search}%"),
                    Book.book_description.ilike(f"%{search}%")
                )
            )
        if category:
            query = query.filter(Book.book_category == category)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, book_id: int) -> Optional[Book]:
        result = await db.execute(select(Book).where(Book.book_id == book_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, book_data: BookCreate) -> Book:
        new_book = Book(**book_data.dict())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book

    async def update(self, db: AsyncSession, book_id: int, update_data: BookUpdate) -> Optional[Book]:
        book = await self.get_by_id(db, book_id)
        if not book:
            return None
        for key, value in update_data.dict(exclude_unset=True).items():
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

    async def get_featured(self, db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Book]:
        result = await db.execute(
            select(Book).where(Book.featured == True).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_popular(self, db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Book]:
        result = await db.execute(
            select(Book).order_by(desc(Book.book_rating)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_new(self, db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Book]:
        result = await db.execute(
            select(Book).order_by(desc(Book.created_at)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def rate_book(self, db: AsyncSession, book_id: int, rating: float) -> Optional[Book]:
        book = await self.get_by_id(db, book_id)
        if not book:
            return None
        book.book_rating = rating
        await db.commit()
        await db.refresh(book)
        return book

    async def toggle_featured(self, db: AsyncSession, book_id: int, featured: bool) -> Optional[Book]:
        book = await self.get_by_id(db, book_id)
        if not book:
            return None
        book.featured = featured
        await db.commit()
        await db.refresh(book)
        return book
