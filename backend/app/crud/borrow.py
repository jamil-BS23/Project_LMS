from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app.models import borrow as borrow_model
from app.schemas import borrow as borrow_schema

def create_borrow(db: Session, request: borrow_schema.BorrowCreate, user_id: int):
    active = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == request.book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if active:
        return None

    borrow = borrow_model.Borrow(
        user_id=user_id,
        book_id=request.book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=request.days or 14),
        status=borrow_model.BorrowStatus.REQUESTED
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.id == borrow.id)\
             .first()

def return_book(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if not borrow: return None
    borrow.return_date = datetime.utcnow()
    borrow.status = borrow_model.BorrowStatus.RETURNED
    db.commit()
    db.refresh(borrow)
    return borrow

def extend_due_date(db: Session, user_id: int, book_id: int, extend_days: int = 7):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if not borrow: return None
    borrow.due_date += timedelta(days=extend_days)
    borrow.extension_count += 1
    db.commit()
    db.refresh(borrow)
    return borrow

def get_user_borrows(db: Session, user_id: int):
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.user_id == user_id)\
             .all()

def get_overdue_borrows(db: Session):
    today = datetime.utcnow()
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(
                 borrow_model.Borrow.return_date.is_(None),
                 borrow_model.Borrow.due_date < today
             ).all()
