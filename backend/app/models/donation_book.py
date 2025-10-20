from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime,Text,Float
from sqlalchemy.orm import relationship
from app.database import Base

class DonationBook(Base):
    __tablename__ = "donation_books"

    donation_book_id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String, index=True, nullable=False)
    book_author = Column(String, index=True, nullable=False)
    donor_name = Column(String, index=True, nullable=False)
    book_category = Column(String, index=True, nullable=False)
    book_description = Column(Text, nullable=True)
    BS_email = Column(String, index=True, nullable=False)
    BS_ID = Column(String, index=True, nullable=False)
    book_image = Column(String, nullable=True)
    book_audio = Column(String, nullable=True)
    book_pdf = Column(String, nullable=True)
    donation_status = Column(String, default="Pending")
    book_copies = Column(Integer, default=1)
