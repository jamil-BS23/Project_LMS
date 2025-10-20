# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # Make sure it's async: postgresql+asyncpg://user:pass@host/dbname

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
