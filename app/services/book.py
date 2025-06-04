from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException

def create_book(db: Session, book_in: BookCreate) -> Book:
    if db.query(Book).filter(Book.isbn == book_in.isbn).first():
        raise HTTPException(status_code=400, detail="ISBN already exists")
    if book_in.count < 0:
        raise HTTPException(status_code=400, detail="Count must be >= 0")
    book = Book(**book_in.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_books(db: Session):
    return db.query(Book).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book_in: BookUpdate):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    update_data = book_in.dict(exclude_unset=True)
    if "isbn" in update_data:
        if db.query(Book).filter(Book.isbn == update_data["isbn"], Book.id != book_id).first():
            raise HTTPException(status_code=400, detail="ISBN already exists")
    if "count" in update_data and update_data["count"] < 0:
        raise HTTPException(status_code=400, detail="Count must be >= 0")
    for key, value in update_data.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return book 