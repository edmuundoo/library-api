from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserInDB
from app.models.user import User
from app.services.auth import AuthService
from app.core.database import get_db
from app.schemas.user import UserBase
from app.core.config import settings
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = AuthService.hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_user(
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
):
    user = db.query(User).filter(User.email == username).first()
    if not user or not AuthService.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = AuthService.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"} 