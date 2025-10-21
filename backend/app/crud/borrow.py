from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.borrow import Borrow
from app.schemas.borrow import BorrowCreate, BorrowUpdate

async def get_borrow(db: AsyncSession, borrow_id: int):
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    return result.scalars().first()

async def get_borrows(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Borrow).offset(skip).limit(limit))
    return result.scalars().all()

async def create_borrow(db: AsyncSession, borrow: BorrowCreate):
    db_borrow = Borrow(**borrow.dict())
    db.add(db_borrow)
    await db.commit()
    await db.refresh(db_borrow)
    return db_borrow

async def update_borrow(db: AsyncSession, borrow_id: int, borrow_update: BorrowUpdate):
    await db.execute(
        update(Borrow)
        .where(Borrow.id == borrow_id)
        .values(**borrow_update.dict(exclude_unset=True))
    )
    await db.commit()
    return await get_borrow(db, borrow_id)
