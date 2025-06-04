from sqlalchemy.orm import Session
from app.models.reader import Reader
from app.schemas.reader import ReaderBase
from fastapi import HTTPException

def create_reader(db: Session, reader_in: ReaderBase) -> Reader:
    if db.query(Reader).filter(Reader.email == reader_in.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    reader = Reader(**reader_in.dict())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader

def get_readers(db: Session):
    return db.query(Reader).all()

def get_reader(db: Session, reader_id: int):
    return db.query(Reader).filter(Reader.id == reader_id).first()

def update_reader(db: Session, reader_id: int, reader_in: dict):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    if "email" in reader_in:
        if db.query(Reader).filter(Reader.email == reader_in["email"], Reader.id != reader_id).first():
            raise HTTPException(status_code=400, detail="Email already exists")
    for key, value in reader_in.items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader

def delete_reader(db: Session, reader_id: int):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(reader)
    db.commit()
    return reader 