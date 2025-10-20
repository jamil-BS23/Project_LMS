from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.book import BookCRUD
from app.database import get_db
from app.schemas.book import BookDetail, BookCreate, BookUpdate, RateBook, UpoadateFeatures
# from app.routers.auth import get_current_user, admin_required

router = APIRouter(prefix="", tags=["Books"])
book_crud = BookCRUD()

# ------------------ Public / Filtered ------------------
@router.get("/", response_model=List[BookDetail])
async def get_books(
    db: AsyncSession = Depends(get_db),
    search: str | None = Query(None),
    category: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    # current_user=Depends(get_current_user)
):
    books = await book_crud.get_all(db, search=search, category=category, skip=skip, limit=limit)
    return books


@router.get("/featured", response_model=List[BookDetail])
async def get_featured_books(
    db: AsyncSession = Depends(get_db),
    skip: int = 0, limit: int = 20
):
    return await book_crud.get_featured(db, skip=skip, limit=limit)


@router.get("/popular", response_model=List[BookDetail])
async def get_popular_books(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 20):
    return await book_crud.get_popular(db, skip=skip, limit=limit)


@router.get("/new", response_model=List[BookDetail])
async def get_new_books(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 20):
    return await book_crud.get_new(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookDetail)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_crud.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ------------------ Admin ------------------
MEDIA_DIR = "media/uploads"
@router.post("/", response_model=BookDetail)
async def create_book(
    book_title: str = Form(...),
    book_category: str = Form(...),
    book_author: str = Form(...),
    book_description: str = Form(None),
    available_copies: int = Form(0),
    featured: bool = Form(False),
    book_availabity: bool = Form(True),
    book_rating: float = Form(0.0),
    book_image: UploadFile = File(None),
    book_pdf: UploadFile = File(None),
    book_audio: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    # Convert form to Pydantic model
    payload = BookCreate(
        book_title=book_title,
        book_category=book_category,
        book_author=book_author,
        book_description=book_description,
        available_copies=available_copies,
        featured=featured,
        book_availabity=book_availabity,
        book_rating=book_rating
    )

    # Save files if uploaded
    import os, shutil
    from pathlib import Path
    from uuid import uuid4
    os.makedirs(MEDIA_DIR, exist_ok=True)

    def save_file(file: UploadFile):
        if not file:
            return None
        suffix = Path(file.filename).suffix
        filename = f"{uuid4().hex}{suffix}"
        file_path = os.path.join(MEDIA_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return f"/{file_path}"

    payload.book_image = save_file(book_image)
    payload.book_pdf = save_file(book_pdf)
    payload.book_audio = save_file(book_audio)

    return await book_crud.create(db, payload)


@router.patch("/{book_id}", response_model=BookDetail)
async def update_book(
    book_id: int,
    book_title: Optional[str] = Form(None),
    book_category: Optional[str] = Form(None),
    book_author: Optional[str] = Form(None),
    book_description: Optional[str] = Form(None),
    available_copies: Optional[int] = Form(None),
    featured: Optional[bool] = Form(None),
    book_availabity: Optional[bool] = Form(None),
    book_rating: Optional[float] = Form(None),
    book_image: Optional[UploadFile] = File(None),
    book_pdf: Optional[UploadFile] = File(None),
    book_audio: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    payload = BookUpdate(
        book_title=book_title,
        book_category=book_category,
        book_author=book_author,
        book_description=book_description,
        available_copies=available_copies,
        featured=featured,
        book_availabity=book_availabity,
        book_rating=book_rating
    )

    # Save files if uploaded
    import os, shutil
    from pathlib import Path
    from uuid import uuid4
    os.makedirs(MEDIA_DIR, exist_ok=True)

    def save_file(file: UploadFile):
        if not file:
            return None
        suffix = Path(file.filename).suffix
        filename = f"{uuid4().hex}{suffix}"
        file_path = os.path.join(MEDIA_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return f"/{file_path}"

    if book_image:
        payload.book_image = save_file(book_image)
    if book_pdf:
        payload.book_pdf = save_file(book_pdf)
    if book_audio:
        payload.book_audio = save_file(book_audio)

    book = await book_crud.update(db, book_id, payload)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await book_crud.delete(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


@router.patch("/rate", response_model=BookDetail)
async def rate_book(payload: RateBook, db: AsyncSession = Depends(get_db)):
    book = await book_crud.rate_book(db, payload.book_id, payload.book_rating)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}/feature", response_model=BookDetail)
async def toggle_feature(book_id: int, payload: UpoadateFeatures, db: AsyncSession = Depends(get_db)):
    book = await book_crud.toggle_featured(db, book_id, payload.featured)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book