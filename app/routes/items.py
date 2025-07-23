from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models, database, auth

router = APIRouter()


@router.post("/books", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, username: str = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter_by(username=username).first()
    db_book = models.Book(title=book.title, owner=user)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
