from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime,Text,Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String, index=True, nullable=False)
    book_category = Column(String, index=True, nullable=False)
    book_author = Column(String, index=True, nullable=False)
    book_description = Column(Text, nullable=True)
    available_copies = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    book_availabity = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)
    book_rating = Column(Float, default=0.0)
    book_image = Column(String, nullable=True)
    book_audio = Column(String, nullable=True)
    book_pdf = Column(String, nullable=True)
    book_reviews = relationship("Review", back_populates="book")
    book_borrows = relationship("Borrow", back_populates="book")

