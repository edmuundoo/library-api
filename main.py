from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.reader import router as reader_router

app = FastAPI()

# Здесь будут подключаться роуты

app.include_router(auth_router)
app.include_router(reader_router)
