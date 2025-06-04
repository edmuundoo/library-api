from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.borrow import borrow_book, return_book
from app.schemas.borrowed_book import BorrowedBookInDB
from pydantic import BaseModel

class BorrowRequest(BaseModel):
    reader_id: int
    book_id: int

router = APIRouter()

@router.post("/borrow/", response_model=BorrowedBookInDB, status_code=status.HTTP_201_CREATED)
def borrow_book_view(
    req: BorrowRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return borrow_book(db, req.reader_id, req.book_id)

@router.post("/return/", response_model=BorrowedBookInDB)
def return_book_view(
    req: BorrowRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return return_book(db, req.reader_id, req.book_id) 