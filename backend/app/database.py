# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://library:tanzil1234@localhost/library_db"


engine = create_engine(
    DATABASE_URL,
    echo=True,  
    future=True  
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)


Base = declarative_base()


def get_db():
    """
    Yield a database session for FastAPI dependency injection.
    Closes the session automatically after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
