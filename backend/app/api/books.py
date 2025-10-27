from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.book import BookCRUD
from app.database import get_db
from app.schemas.book import BookDetail, BookCreate, BookUpdate, RateBook, UpoadateFeatures
from app.core.security import get_current_user, get_current_admin
from app.models.user import User
from app.utils.minio_utils import upload_file
from fastapi_pagination import Page, paginate 

router = APIRouter(prefix="", tags=["Books"])
book_crud = BookCRUD()

@router.get("/", response_model=Page[BookDetail])
async def get_books(
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by title, author, or description"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    books = await book_crud.get_all(db, search=search, category=category)
    return paginate(books)



@router.get("/featured_book", response_model=List[BookDetail])
async def get_featured_books(
    db: AsyncSession = Depends(get_db),
    skip: int = 0, limit: int = 20
):
    return await book_crud.get_featured(db, skip=skip, limit=limit)


@router.get("/popular", response_model=List[BookDetail])
async def get_popular_books(db: AsyncSession = Depends(get_db),
                            skip: int = 0, limit: int = 20):
    return await book_crud.get_popular(db, skip=skip, limit=limit)


@router.get("/new", response_model=List[BookDetail])
async def get_new_books(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 20):
    return await book_crud.get_new(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookDetail)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = await book_crud.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


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
    current_user: User = Depends(get_current_admin)
):
    
    photo_url = upload_file(book_image, folder="books")
    pdf_url = upload_file(book_pdf, folder="book_pdfs") if book_pdf else None
    audio_url = upload_file(book_audio, folder="book_audios") if book_audio else None
    # Convert form to Pydantic model
    payload = BookCreate(
        book_title=book_title,
        book_category=book_category,
        book_author=book_author,
        book_description=book_description,
        available_copies=available_copies,
        featured=featured,
        book_availabity=book_availabity,
        book_rating=book_rating,
        book_image=photo_url,
        book_pdf=pdf_url,
        book_audio=audio_url
    )

    # Save files if uploaded

    return await book_crud.create(db, payload)


@router.patch("/{book_id}", response_model=BookDetail)
async def update_book(
    book_id: int,
    form_data: BookUpdate = Depends(BookUpdate.as_form),
    book_image: Optional[UploadFile] = File(None),
    book_pdf: Optional[UploadFile] = File(None),
    book_audio: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    photo_url = upload_file(book_image, folder="books")
    pdf_url = upload_file(book_pdf, folder="book_pdfs") if book_pdf else None
    audio_url = upload_file(book_audio, folder="book_audios") if book_audio else None
    update_fields = form_data.dict(exclude_unset=True)
    if photo_url:
        update_fields["book_image"] = photo_url
    if pdf_url:
        update_fields["book_pdf"] = pdf_url
    if audio_url:
        update_fields["book_audio"] = audio_url

    book = await book_crud.update(db, book_id, BookUpdate(**update_fields))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    deleted = await book_crud.delete(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


@router.patch("/{book_id}/feature", response_model=BookDetail)
async def toggle_feature(book_id: int, payload: UpoadateFeatures, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_admin)):
    book = await book_crud.toggle_featured(db, book_id, payload.featured)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book