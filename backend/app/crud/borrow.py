from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models.borrow import BorrowRecord
from app.models.book import Book
from app.models.user import User
from app.schemas.borrow import BorrowCreate, BorrowStatusUpdate, BorrowDetailResponse
from fastapi import HTTPException, status
from datetime import date, timedelta, datetime
from app.crud.settings import SettingsCRUD  
from sqlalchemy import func
from datetime import datetime, date




class BorrowCRUD:

    @staticmethod
    async def get_borrow(db: AsyncSession, borrow_id: int) -> BorrowRecord:
        borrow = await db.get(BorrowRecord, borrow_id)
        if not borrow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BORROW_RECORD_NOT_FOUND"
            )
        return borrow

    @staticmethod
    async def get_all_borrows(db: AsyncSession, skip: int = 0, limit: int = 20):
        result = await db.execute(
            select(BorrowRecord).offset(skip).limit(limit)
        )
        return result.scalars().all()

    
    @staticmethod
    async def count_by_borrow_status(db: AsyncSession, status: str) -> int:
        """
        Count number of borrows by borrow_status.
        """
        result = await db.execute(
            select(func.count()).select_from(BorrowRecord).where(BorrowRecord.borrow_status == status)
        )
        return result.scalar_one()


    @staticmethod
    async def create_pdf_borrow(db: AsyncSession, user: User, book_id: int):
        book = await db.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if not book.book_pdf:
            raise HTTPException(status_code=400, detail="PDF not available for this book")
        

        existing_borrow = await db.execute(
        select(BorrowRecord)
        .where(BorrowRecord.user_id == user.user_id, BorrowRecord.book_id == book_id, BorrowRecord.borrow_status == "pdf-viewed")
        )
        existing_borrow = existing_borrow.scalars().first()

        if existing_borrow:
            return existing_borrow

        today = date.today()
        db_borrow = BorrowRecord(
            user_id=user.user_id,
            book_id=book.book_id,
            borrow_date=today,
            return_date=today,
            borrow_status="pdf-viewed",
        )
        db.add(db_borrow)
        await db.commit()
        await db.refresh(db_borrow)
        return db_borrow



    @staticmethod
    async def create_borrow(db: AsyncSession, borrow: "BorrowCreate", user: User):
        # 1️⃣ Get the book
        book = await db.get(Book, borrow.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="BOOK_NOT_FOUND")

        # 2️⃣ Check book availability
        if not book.book_availabity or (book.available_copies is not None and book.available_copies < 1):
            raise HTTPException(status_code=409, detail="BOOK_UNAVAILABLE")

        # 3️⃣ Fetch borrow_day_limit from settings
        borrow_day_limit = await SettingsCRUD.get_borrow_day_limit(db)
        if borrow_day_limit is None:
            raise HTTPException(status_code=500, detail="BORROW_LIMIT_NOT_SET")

        # 4️⃣ Borrow max limit (can later come from Settings)
        borrow_max_limit = await SettingsCRUD.get_borrow_max_limit(db)

        # 5️⃣ Check if user already borrowed this book without returning it
        existing_borrow = await db.execute(
            select(BorrowRecord)
            .where(BorrowRecord.user_id == user.user_id)
            .where(BorrowRecord.book_id == borrow.book_id)
            .where(BorrowRecord.borrow_status != "returned")
            .where(BorrowRecord.borrow_status != "rejected")
            .where(BorrowRecord.borrow_status != "pdf-viewed")
        )
        existing_borrow = existing_borrow.scalars().first()
        if existing_borrow:
            raise HTTPException(status_code=409, detail="USER_ALREADY_BORROWED_THIS_BOOK")

        # 6️⃣ Check total borrowed books for user
        total_active_borrows = await db.execute(
            select(func.count())
            .select_from(BorrowRecord)
            .where(BorrowRecord.user_id == user.user_id)
            .where(BorrowRecord.borrow_status != "returned")
            .where(BorrowRecord.borrow_status != "rejected")
            .where(BorrowRecord.borrow_status != "pdf-viewed")
        )
        total_active_borrows = total_active_borrows.scalar() or 0
        if total_active_borrows >= borrow_max_limit:
            raise HTTPException(
                status_code=409,
                detail=f"USER_CANNOT_BORROW_MORE_THAN_{borrow_max_limit}_BOOKS"
            )

        borrow_date = date.today()
        return_date = borrow_date + timedelta(days=borrow_day_limit)

        if getattr(borrow, "return_date", None):
            try:
                requested_return_date = borrow.return_date
                if isinstance(requested_return_date, str):
                    requested_return_date = datetime.strptime(requested_return_date, "%m/%d/%Y").date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="INVALID_DATE_FORMAT_EXPECTED_MM_DD_YYYY"
                )

            max_allowed_date = borrow_date + timedelta(days=borrow_day_limit)
            if requested_return_date > max_allowed_date:
                raise HTTPException(
                    status_code=400,
                    detail=f"RETURN_DATE_CANNOT_EXCEED_{borrow_day_limit}_DAYS_FROM_TODAY"
                )
            return_date = requested_return_date

        
        db_borrow = BorrowRecord(
            user_id=user.user_id,
            book_id=book.book_id,
            borrow_date=borrow_date,
            return_date=return_date,
            borrow_status="pending",
        )

        db.add(db_borrow)

        # 9️⃣ Update book availability
        if book.available_copies is not None and book.available_copies > 0:
            book.available_copies -= 1
        book.book_availabity = book.available_copies > 0
        db.add(book)

        # 🔟 Commit transaction
        await db.commit()
        await db.refresh(db_borrow)

        return db_borrow

#     @staticmethod
#     async def create_borrow(db: AsyncSession, borrow: BorrowCreate, user: User):
#         # Get book
#         book = await db.get(Book, borrow.book_id)
#         if not book:
#             raise HTTPException(status_code=404, detail="BOOK_NOT_FOUND")

#         # Validate availability
#         if not book.book_availabity:
#             raise HTTPException(status_code=409, detail="BOOK_UNAVAILABLE")

#         borrow_day_limit = await SettingsCRUD.get_borrow_day_limit(db) 
#         borrow_day_limit = borrow_day_limit if borrow_day_limit is not None else 14

#         # Borrow/Return dates auto-set
#         borrow_date = date.today()
#         return_date = borrow_date + timedelta(days=borrow_day_limit)         

#         # Create borrow record
#         db_borrow = BorrowRecord(
#             user_id=user.user_id,
#             #user_name=user.user_name,   
#             book_id=book.book_id,
#             #book_title=book.book_title,      
#             borrow_date=borrow_date,
#             return_date=return_date,
#             borrow_status="pending",

#         )

#         print("all info: ", db_borrow)
      
#         db.add(db_borrow)

# # --- Update book availability based on count ---
# # Decrease the count of available copies
#         if book.book_availabity is not None and book.available_copies > 0:
#             book.available_copies -= 1

# # If no copies left, mark as unavailable
#         if book.available_copies == 0:
#             book.book_availabity = False
#         else:
#             book.book_availabity = True  # remains available if count > 0

#         db.add(book)

#         await db.commit()
#         await db.refresh(db_borrow)
#         return db_borrow


    # @staticmethod
    # async def create_borrow(db: AsyncSession, borrow: "BorrowCreate", user: User):
    #     book = await db.get(Book, borrow.book_id)
    #     if not book:
    #         raise HTTPException(status_code=404, detail="BOOK_NOT_FOUND")

    #     if not book.book_availabity or (book.available_copies is not None and book.available_copies < 1):
    #         raise HTTPException(status_code=409, detail="BOOK_UNAVAILABLE")

    #     borrow_day_limit = await SettingsCRUD.get_borrow_day_limit(db)
    #     if borrow_day_limit is None:
    #         raise HTTPException(status_code=500, detail="BORROW_LIMIT_NOT_SET")

    #     borrow_max_limit = 5

    #     existing_borrow = await db.execute(
    #         select(BorrowRecord)
    #         .where(BorrowRecord.user_id == user.user_id)
    #         .where(BorrowRecord.book_id == borrow.book_id)
    #         .where(BorrowRecord.borrow_status != "returned")
    #     )
    #     existing_borrow = existing_borrow.scalars().first()
    #     if existing_borrow:
    #         raise HTTPException(status_code=409, detail="USER_ALREADY_BORROWED_THIS_BOOK")

    #     total_active_borrows = await db.execute(
    #         select(func.count())
    #         .select_from(BorrowRecord)
    #         .where(BorrowRecord.user_id == user.user_id)
    #         .where(BorrowRecord.borrow_status != "returned")
    #     )
    #     total_active_borrows = total_active_borrows.scalar() or 0
    #     if total_active_borrows >= borrow_max_limit:
    #         raise HTTPException(
    #             status_code=409,
    #             detail=f"USER_CANNOT_BORROW_MORE_THAN_{borrow_max_limit}_BOOKS"
    #         )

    #     borrow_date = date.today()
    #     requested_return_date = getattr(borrow, "return_date", None)

    #     if requested_return_date:
    #         try:
    #             if isinstance(requested_return_date, str):
    #                 requested_return_date = datetime.strptime(requested_return_date, "%m/%d/%Y").date()
    #         except ValueError:
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail="INVALID_DATE_FORMAT_EXPECTED_MM_DD_YYYY"
    #             )

    #         if requested_return_date > date.today() + timedelta(days=borrow_day_limit):
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail=f"RETURN_DATE_CANNOT_EXCEED_{borrow_day_limit}_DAYS"
    #             )
    #         return_date = requested_return_date
    #     else:
    #         return_date = date.today() + timedelta(days=borrow_day_limit)

        
    #     db_borrow = BorrowRecord(
    #         user_id=user.user_id,
    #         book_id=book.book_id,
    #         borrow_date=borrow_date,
    #         return_date=return_date,
    #         borrow_status="pending",
    #     )

      
    #     db.add(db_borrow)

    #     if book.available_copies is not None and book.available_copies > 0:
    #         book.available_copies -= 1
    #     book.book_availabity = book.available_copies > 0
    #     db.add(book)

    #     await db.commit()
    #     await db.refresh(db_borrow)

    #     return db_borrow



    @staticmethod
    async def list_by_borrow_status(db: AsyncSession, status: str):
        """
        Get detailed list of borrows filtered by borrow_status.
        """
        result = await db.execute(
            select(BorrowRecord).where(BorrowRecord.borrow_status == status)
        )
        borrows = result.scalars().all()

        for borrow in borrows:
            book = await db.get(Book, borrow.book_id)
            borrow.book_title = book.book_title if book else None

            user = await db.get(User, borrow.user_id)
            borrow.user_email = user.user_email
            borrow.user_name = user.user_name if user else None
            borrow.user_email = user.user_email if user else None
        
       
        return borrows




    @staticmethod
    async def list_by_request_status(db: AsyncSession, status: str):
        """
        Get detailed list of borrows filtered by request_status.
        """
        result = await db.execute(
            select(BorrowRecord).where(BorrowRecord.request_status == status)
        )
        borrows = result.scalars().all()


        for borrow in borrows:
            book = await db.get(Book, borrow.book_id)
            borrow.book_title = book.book_title if book else None

            user = await db.get(User, borrow.user_id)
            borrow.user_name = user.user_name if user else None

        return borrows




    @staticmethod
    async def get_all_borrows_admin(db: AsyncSession):
        """
        Admin: Get all borrow records for all users with book & user details.
        """
        result = await db.execute(select(BorrowRecord))
        borrows = result.scalars().all()

        for borrow in borrows:
            book = await db.get(Book, borrow.book_id)
            borrow.book_title = book.book_title if book else None

            user = await db.get(User, borrow.user_id)
            borrow.user_name = user.user_name if user else None

        return borrows







    @staticmethod
    async def get_my_borrow(db: AsyncSession, user_id: str):
        """
        Get all borrow records for a specific user with book/user details.
        """
        result = await db.execute(
            select(BorrowRecord).where(BorrowRecord.user_id == user_id)
        )
        borrows = result.scalars().all()

        for borrow in borrows:
            book = await db.get(Book, borrow.book_id)
            borrow.book_title = book.book_title if book else None

            user = await db.get(User, borrow.user_id)
            borrow.user_name = user.user_name if user else None

        return borrows


    @staticmethod
    async def count_my_borrow_status(db: AsyncSession, user_id: str, status: str) -> int:
   
        now = datetime.utcnow().date()  # ✅ Convert to date only

    # Fetch all user's active borrows
        result = await db.execute(
            select(BorrowRecord).where(
                BorrowRecord.user_id == user_id,
                BorrowRecord.borrow_status != "returned"
            )
        )
        user_borrows = result.scalars().all()

    # Update overdue borrows
        updated = False
        for borrow in user_borrows:
        # ✅ Ensure both are date objects for safe comparison
            if borrow.return_date and borrow.return_date < now and borrow.borrow_status != "overdue":
                borrow.borrow_status = "overdue"
                db.add(borrow)
                updated = True

        if updated:
            await db.commit()

    # Count the requested status
        result = await db.execute(
            select(func.count()).select_from(BorrowRecord).where(
            BorrowRecord.user_id == user_id,
            BorrowRecord.borrow_status == status
        )
        )
        return result.scalar_one()

    
    # @staticmethod
    # async def count_my_borrow_status(db: AsyncSession, user_id: str, status: str) -> int:
    #     """
    #     Count borrows for a specific user filtered by borrow_status.
    #     Async-safe ORM query using select().
    #     """
    #     result = await db.execute(
    #         select(func.count()).select_from(BorrowRecord).where(
    #             BorrowRecord.user_id == user_id,
    #             BorrowRecord.borrow_status == status
    #         )
    #     )
    #     return result.scalar_one()


        if updated:
            await db.commit()

        result = await db.execute(
            select(func.count()).select_from(BorrowRecord).where(
            BorrowRecord.user_id == user_id,
            BorrowRecord.borrow_status == status
        )
        )
        return result.scalar_one()

    



    @staticmethod
    async def count_by_request_status(db: AsyncSession, status: str) -> int:
        """
        Count number of borrows by request_status.
        """
        result = await db.execute(
            select(func.count()).select_from(BorrowRecord).where(BorrowRecord.request_status == status)
        )
        return result.scalar_one()
    


    @staticmethod
    async def update_borrow_status(db: AsyncSession, borrow_id: int, status: str):
        # Fetch the borrow record
        db_borrow = await db.get(BorrowRecord, borrow_id)
        if not db_borrow:
            raise HTTPException(status_code=404, detail="BORROW_NOT_FOUND")

        # Update the status
        db_borrow.borrow_status = status

        # ✅ If returned, set returned_at to today's date and update book availability
        if status == "returned":
            db_borrow.returned_at = datetime.utcnow().date()  # set today's date

            # Update the book's available copies
            book = await db.get(Book, db_borrow.book_id)
            if book:
                book.available_copies = (book.available_copies or 0) + 1
                db.add(book)

        if status == "rejected":
            # Update the book's available copies
            book = await db.get(Book, db_borrow.book_id)
            if book:
                book.book_availabity = True
                book.available_copies = (book.available_copies or 0) + 1
                db.add(book)
        db.add(db_borrow)
        await db.commit()
        await db.refresh(db_borrow)

        # Fetch related user and book for response
        user = await db.get(User, db_borrow.user_id)
        book = await db.get(Book, db_borrow.book_id)

        return BorrowDetailResponse(
            borrow_id=db_borrow.borrow_id,
            user_id=db_borrow.user_id,
            user_name=user.user_name if user else None,
            book_id=db_borrow.book_id,
            book_title=book.book_title if book else None,
            borrow_date=db_borrow.borrow_date,
            return_date=db_borrow.return_date,
            borrow_status=db_borrow.borrow_status,
            returned_at=db_borrow.returned_at if hasattr(db_borrow, "returned_at") else None
        )


    # @staticmethod
    # async def update_borrow_status(db: AsyncSession, borrow_id: int, status: str):


    #     db_borrow = await db.get(BorrowRecord, borrow_id)
    #     if not db_borrow:
    #         raise HTTPException(status_code=404, detail="BORROW_NOT_FOUND")

    #     # Update status
    #     db_borrow.borrow_status = status

    #     # If returned, make book available and increment count
    #     if status == "returned":
    #         book = await db.get(Book, db_borrow.book_id)
    #         if book:
    #             book.available_copies = (book.available_copies or 0) + 1
    #             db.add(book)

    #     db.add(db_borrow)
    #     await db.commit()
    #     await db.refresh(db_borrow)

    # # Fetch related user and book for response
    #     user = await db.get(User, db_borrow.user_id)
    #     book = await db.get(Book, db_borrow.book_id)

    #     return BorrowDetailResponse(
    #         borrow_id=db_borrow.borrow_id,
    #         user_id=db_borrow.user_id,
    #         user_name=user.user_name if user else None,
    #         book_id=db_borrow.book_id,
    #         book_title=book.book_title if book else None,
    #         borrow_date=db_borrow.borrow_date,
    #         return_date=db_borrow.return_date,
    #         borrow_status=db_borrow.borrow_status
    #     )
    





    @staticmethod
    async def update_borrow_request_status(db: AsyncSession, borrow_id: int, status: str):


        db_borrow = await db.get(BorrowRecord, borrow_id)
        if not db_borrow:
            raise HTTPException(status_code=404, detail="BORROW_NOT_FOUND")

        # Update status
        db_borrow.request_status = status

        # If returned, make book available and increment count
        if status == "accepted":
            book = await db.get(Book, db_borrow.book_id)
            if book:
                book.book_availability = True
                book.book_copies = (book.book_copies or 0) - 1
                db.add(book)

        db.add(db_borrow)
        await db.commit()
        await db.refresh(db_borrow)

    # Fetch related user and book for response
        user = await db.get(User, db_borrow.user_id)
        book = await db.get(Book, db_borrow.book_id)

        return BorrowDetailResponse(
            borrow_id=db_borrow.borrow_id,
            user_id=db_borrow.user_id,
            user_name=user.user_name if user else None,
            book_id=db_borrow.book_id,
            book_title=book.book_title if book else None,
            borrow_date=db_borrow.borrow_date,
            return_date=db_borrow.return_date,
            borrow_status=db_borrow.borrow_status,
            request_status=db_borrow.request_status,
        )








    @staticmethod
    async def delete_borrow(db: AsyncSession, db_borrow: BorrowRecord):
        # If deleting an active borrow, free the book
        if db_borrow.borrow_status == "borrowed":
            book = await db.get(Book, db_borrow.book_id)
            if book:
                book.book_availability = True
                db.add(book)

        await db.delete(db_borrow)
        await db.commit()
        return True


           
    @staticmethod
    async def list_my_borrow_status(db: AsyncSession, status: str, user_id: str = None):
    
        query = select(BorrowRecord).where(BorrowRecord.borrow_status == status)

        if user_id:
            query = query.where(BorrowRecord.user_id == user_id)

        result = await db.execute(query)
        borrows = result.scalars().all()

    # Add book_title and user_name
        for borrow in borrows:
            book = await db.get(Book, borrow.book_id)
            borrow.book_title = book.book_title if book else None

            user = await db.get(User, borrow.user_id)
            borrow.user_name = user.user_name if user else None

        return borrows



    @staticmethod
    async def count_my_request_status(db: AsyncSession, status: str, user_id: str = None) -> int:
  
        query = select(func.count()).select_from(BorrowRecord).where(BorrowRecord.request_status == status)

        if user_id:
            query = query.where(BorrowRecord.user_id == user_id)

        result = await db.execute(query)
        return result.scalar_one()



    @staticmethod
    async def list_my_request_status(db: AsyncSession, status: str, user_id: str = None):
    
        query = select(BorrowRecord).where(BorrowRecord.request_status == status)

        if user_id:
            query = query.where(BorrowRecord.user_id == user_id)

        result = await db.execute(query)
        borrows = result.scalars().all()

        for borrow in borrows:
            book = await db.get(Book, borrow.book_id)
            borrow.book_title = book.book_title if book else None

            user = await db.get(User, borrow.user_id)
            borrow.user_name = user.user_name if user else None

        return borrows















