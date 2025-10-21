from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from app.database import Base
from datetime import datetime

class Borrow(Base):
    __tablename__ = "borrow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending", nullable=False)
