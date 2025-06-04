from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BorrowedBookBase(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: Optional[datetime] = None
    return_date: Optional[datetime] = None

class BorrowedBookCreate(BaseModel):
    book_id: int
    reader_id: int

class BorrowedBookUpdate(BaseModel):
    return_date: Optional[datetime] = None

class BorrowedBookInDB(BorrowedBookBase):
    id: int

    class Config:
        orm_mode = True 