from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import borrow  # your borrow router

from app.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0")

# Include borrow router
app.include_router(borrow.router, prefix="/api/borrows")

@app.get("/")
def root():
    return {"message": "Library API running!"}
