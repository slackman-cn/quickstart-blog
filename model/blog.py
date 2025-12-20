from typing import Optional
from schema import BlogBase
from sqlmodel import Field, Session, SQLModel


class BlogPublic(BlogBase):
    id: int
    user_name: str

class BlogCreate(BlogBase):
    content_rich: Optional[str] = None

class BlogUpdate(SQLModel):
    title: Optional[str] = None
    summary: Optional[str] = None