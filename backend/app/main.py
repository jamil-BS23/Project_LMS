import asyncio
from fastapi import FastAPI
from app.api import auth, users, books, categories, borrow, admin,  uploads, settings, donation_book, rate_book, book_review
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination



app = FastAPI()
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(uploads.router, prefix="/files")
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(borrow.router, prefix="", tags=["Borrow"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])
app.include_router(donation_book.router, prefix="/donation", tags=["Donation Book"])
app.include_router(rate_book.router, prefix="/rate_book", tags=["Rate Book"])
app.include_router(book_review.router, prefix="/book_review", tags=["Book Review"])


@app.get("/")
async def root():
    return {
        "message": "Library Backend API is running",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

