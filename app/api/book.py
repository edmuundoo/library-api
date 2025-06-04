from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.book import BookCreate, BookUpdate, BookInDB
from app.services.book import create_book, get_books, get_book, update_book, delete_book
from typing import List

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookInDB, status_code=status.HTTP_201_CREATED)
def create_book_view(book_in: BookCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_book(db, book_in)

@router.get("/", response_model=List[BookInDB])
def read_books_view(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_books(db)

@router.put("/{book_id}", response_model=BookInDB)
def update_book_view(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_book(db, book_id, book_in)

@router.delete("/{book_id}", response_model=BookInDB)
def delete_book_view(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return delete_book(db, book_id) 