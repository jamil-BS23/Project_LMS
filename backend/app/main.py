from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import borrow  # Correct import

from app.database import Base, engine

# Create tables (for dev only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(borrow.router, prefix="/api/borrows")

@app.get("/")
def root():
    return {"message": "Library API running!"}
