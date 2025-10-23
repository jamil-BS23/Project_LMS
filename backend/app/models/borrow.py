from sqlalchemy import Column, Integer, ForeignKey, Date, String
from app.database import Base

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    borrow_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.book_id", ondelete="CASCADE"))
    borrow_date = Column(Date)
    return_date = Column(Date, nullable=True)
    returned_at = Column(Date, nullable=True)
    borrow_status = Column(String(50), default="pending")





