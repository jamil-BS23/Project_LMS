from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.donation_book import DonationBook
from app.models.book import Book
from app.models.category import Category

class DonationBookCRUD:


    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(DonationBook))
        return result.scalars().all()



    @staticmethod
    async def create_request(db: AsyncSession, data: dict):
        # ensure category exists

        db_obj = DonationBook(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


    @staticmethod
    async def get_by_status(db: AsyncSession, status: str):
        result = await db.execute(select(DonationBook).where(DonationBook.donation_status == status))
        return result.scalars().all()

    @staticmethod
    async def update_donation_status(db: AsyncSession, d_book_id: int, new_status: str):
        # Fetch the donation request
        result = await db.execute(select(DonationBook).where(DonationBook.donation_book_id == d_book_id))
        donation = result.scalar_one_or_none()
        if not donation:
            raise HTTPException(status_code=404, detail="Donation request not found")
        

        # Update the status
        donation.donation_status = new_status

        # If status is 'approved', insert into books table
        if new_status == "accepted":
            new_book = Book(
                book_title=donation.book_title,
                book_author=donation.book_author,
                book_category=donation.book_category,
                book_image=donation.book_image,
                book_pdf=donation.book_pdf,
                book_audio=donation.book_audio,
                book_description=donation.book_description,
                available_copies=donation.book_copies,
            )
            db.add(new_book)

        await db.commit()
        await db.refresh(donation)
        return donation
