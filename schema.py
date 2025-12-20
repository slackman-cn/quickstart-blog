from typing import Optional
from typing import Annotated
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, UniqueConstraint, create_engine, select


class UserBase(SQLModel):
    username: str = Field(unique=True)
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

## 文章publish之后 ++,  文章记录code属性
class PageCategoryBase(SQLModel):
    code: str = Field(unique=True)
    name: str
    remark: Optional[str] = None # category详情，tag颜色
    blog_count: int = 0
    sort_order: int = 0

class PageCategory(PageCategoryBase, table=True):
    __tablename__ = 'page_category'
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

## 文章create之后++,  删除文章不删除tag。输入标签input，先检索tag
class PageTagBase(SQLModel):
    name: str
    blog_id: int

class PageTag(PageTagBase, table=True):
    __tablename__ = 'page_tag'
    __table_args__ = (
        UniqueConstraint("name", "blog_id", name="uq_tag_blog"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

class BlogBase(SQLModel):
    title: str
    category_code: str
    summary: Optional[str] = None # 摘要
    num_read: Optional[int] = 0 # 浏览次数
    num_star: Optional[int] = 0 # 收藏次数
    num_reply: Optional[int] = 0 # 评论次数
    num_thumb: Optional[int] = 0 # 点赞次数
    is_top: bool = False # 是否置顶
    status: Optional[str] = Field(default='SAVE_SUBMIT') # 暂存，发布中，已发布 ENUM('DRAFT', 'PUBLISHED', 'ARCHIVED') DEFAULT 'DRAFT'
    allow_comment: bool = True
    publish_time: Optional[datetime] = None

class Blog(BlogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content_rich: Optional[str] = None
    user_name: Optional[str] = None
    user_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BlogLikeBase(SQLModel):
    blog_title: str
    blog_id: str
    mode: str = 'star' # 点赞，收藏
    user_name: Optional[str] = None
    user_id: Optional[str] = None

class BlogLike(BlogLikeBase, table=True):
    __tablename__ = 'blog_like'
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
    __tablename__ = 'blog_reply'
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

def init_user():

    user1 = User(username='admin', nickname='管理员', email='admin@example.com',
                 password_hash='$2b$12$XNBdL2iNdo4YNFB2GH/2wO4IN0VsDXTticOcrd.UgD50tReiIrTiu', user_role='ADMIN')
    user2 = User(username='demo', nickname='演示用户', email='demo@example.com',
                 password_hash='$2b$12$XNBdL2iNdo4YNFB2GH/2wO4IN0VsDXTticOcrd.UgD50tReiIrTiu')

    category1 = PageCategory(code="default", name="默认分组")
    with Session(engine) as session:
        session.add(user1)
        session.add(user2)
        session.add(category1)
        session.commit()