import asyncio
from fastapi import FastAPI
from app.api import books
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(books.router, prefix="/books", tags=["Books"])





@app.get("/")
async def root():
    return {
        "message": "📚 Library Backend API is running 🚀",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
