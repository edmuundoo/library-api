from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.reader import Reader
from app.schemas.reader import ReaderBase, ReaderInDB
from app.services.reader import create_reader, get_readers, get_reader, update_reader, delete_reader
from typing import List

router = APIRouter(prefix="/readers", tags=["readers"])

@router.post("/", response_model=ReaderInDB, status_code=status.HTTP_201_CREATED)
def create_reader_view(reader_in: ReaderBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_reader(db, reader_in)

@router.get("/", response_model=List[ReaderInDB])
def read_readers_view(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_readers(db)

@router.put("/{reader_id}", response_model=ReaderInDB)
def update_reader_view(reader_id: int, reader_in: dict = Body(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_reader(db, reader_id, reader_in)

@router.delete("/{reader_id}", response_model=ReaderInDB)
def delete_reader_view(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return delete_reader(db, reader_id) 