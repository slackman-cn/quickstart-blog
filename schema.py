from typing import Optional
from typing import Annotated
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class UserBase(SQLModel):
    username: str
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    user_status: Optional[str] = Field(default='ACTIVE') # ENUM('ACTIVE', 'INACTIVE', 'BANNED') DEFAULT 'ACTIVE'
    user_role: Optional[str] = Field(default='USER') # ENUM('USER', 'ADMIN') DEFAULT 'USER'

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class PageMetaBase(SQLModel):
    type: str = 'category'  # tag | category
    name: str = '默认分类'
    slug: Optional[str] = None # 'default'
    remark: Optional[str] = None # category详情，tag颜色
    blog_count: int = 0
    sort_order: int = 0

class PageMeta(PageMetaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BlogBase(SQLModel):
    title: str
    user_name: str
    user_id: str
    category_name: str
    summary: Optional[str] = None # 摘要
    content_rich: Optional[str] = None
    num_read: Optional[int] = None # 浏览次数
    num_star: Optional[int] = None # 收藏次数
    num_reply: Optional[int] = None # 评论次数
    num_thumb: Optional[int] = None # 点赞次数
    is_top: bool = False # 是否置顶
    status: Optional[str] = None # 暂存，发布中，已发布 ENUM('DRAFT', 'PUBLISHED', 'ARCHIVED') DEFAULT 'DRAFT'
    allow_comment: bool = True
    publish_time: Optional[datetime] = None

class Blog(BlogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BlogTagBase(SQLModel):
    blog_title: str
    blog_id: str
    tag_name: Optional[str] = None


class BlogTag(BlogTagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BlogLikeBase(SQLModel):
    blog_title: str
    blog_id: str
    mode: str = 'star' # 点赞，收藏
    user_name: Optional[str] = None
    user_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class BlogLike(BlogLikeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class BlogReplyBase(SQLModel):
    blog_title: str
    blog_id: str
    parent_id: Optional[str] = None
    content_text: str  # 评论内容
    status: Optional[str] = None  # ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'APPROVED' COMMENT '评论状态'

class BlogReply(BlogReplyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


## init
sqlite_url = "sqlite:///schema.db"
# sqlite_url = "sqlite+pysqlite:///:memory:"

engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield  session

SessionDep = Annotated[Session, Depends(get_session)]
