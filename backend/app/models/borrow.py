from sqlalchemy import Column, Integer, Date, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class BorrowStatus(enum.Enum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
    REJECTED = "REJECTED"

class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False) 
    book_id = Column(Integer, nullable=False) 
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(Enum(BorrowStatus, name="borrowstatus"), nullable=False)
    extension_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
