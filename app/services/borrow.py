from sqlalchemy.orm import Session
from app.models.borrowed_book import BorrowedBook
from app.models.book import Book
from app.models.reader import Reader
from fastapi import HTTPException
from datetime import datetime

def borrow_book(db: Session, reader_id: int, book_id: int) -> BorrowedBook:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.count < 1:
        raise HTTPException(status_code=400, detail="No available copies")
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    active_borrows = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date == None
    ).count()
    if active_borrows >= 3:
        raise HTTPException(status_code=400, detail="Borrow limit reached")
    borrowed = BorrowedBook(book_id=book_id, reader_id=reader_id)
    db.add(borrowed)
    book.count -= 1
    db.commit()
    db.refresh(borrowed)
    return borrowed

def return_book(db: Session, reader_id: int, book_id: int) -> BorrowedBook:
    borrow = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.book_id == book_id,
        BorrowedBook.return_date == None
    ).first()
    if not borrow:
        raise HTTPException(status_code=400, detail="No active borrow found")
    borrow.return_date = datetime.utcnow()
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.count += 1
    db.commit()
    db.refresh(borrow)
    return borrow 