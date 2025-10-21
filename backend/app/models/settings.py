from sqlalchemy import Column, Integer
from sqlalchemy.sql import func
from app.database import Base

class Settings(Base):
    __tablename__ = "settings"

    setting_id = Column(Integer, primary_key=True, autoincrement=True)
    borrow_day_limit = Column(Integer, nullable=False)
    borrow_day_extension_limit = Column(Integer, nullable=False)
    borrow_max_limit = Column(Integer, nullable=False)
    booking_duration= Column(Integer, nullable=False)
    booking_days_limit = Column(Integer, nullable=False)