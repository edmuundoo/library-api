from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.reader import Reader
from app.schemas.reader import ReaderInDB
from typing import List

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/", response_model=List[ReaderInDB])
def get_readers(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Reader).all() 