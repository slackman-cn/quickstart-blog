from typing import Optional
from schema import PageCategoryBase
from sqlmodel import Field, Session, SQLModel

class PageCategoryPublic(PageCategoryBase):
    id: int

class PageCategoryCreate(SQLModel):
    code: str
    name: str
    remark: Optional[str] = None

class PageCategoryUpdate(SQLModel):
    name: Optional[str] = None
    remark: Optional[str] = None