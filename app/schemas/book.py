from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    count: int
    description: Optional[str] = None  # добавляем поле description

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    count: Optional[int] = None
    description: Optional[str] = None  # добавляем поле description

class BookInDB(BookBase):
    id: int

    class Config:
        orm_mode = True