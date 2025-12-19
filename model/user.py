from typing import Optional
from schema import UserBase
from sqlmodel import Field, Session, SQLModel

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None