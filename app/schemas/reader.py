from pydantic import BaseModel

class ReaderBase(BaseModel):
    name: str
    email: str

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    name: str = None
    email: str = None

class ReaderInDB(ReaderBase):
    id: int

    class Config:
        orm_mode = True 