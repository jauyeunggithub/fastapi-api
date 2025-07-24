from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database, auth

router = APIRouter()

# Use this or import from your database module


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/books", response_model=schemas.BookOut)
def create_book(
    book: schemas.BookCreate,
    # assuming this returns User object
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Optionally verify current_user exists in DB (should already be verified in auth)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # assuming owner_id FK
    db_book = models.Book(title=book.title, owner_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
