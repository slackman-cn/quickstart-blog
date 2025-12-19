# pip install sqlmodel
# mysql驱动
# pip install pymysql
# postgresql驱动
# pip install psycopg2-binary

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, create_engine
from sqlmodel import Field, Session, BigInteger, Integer, String, Boolean

# 内存
db_url = "sqlite+pysqlite:///:memory:"
# sqlite
# db_url = "sqlite+pysqlite:///db_demo.sqlite"
# mysql
# db_url = "mysql+pymysql://username:password@192.168.1.1:3306/db_demo"
# postgresql
# db_url = "postgresql://username:password@192.168.1.1:5432/db_demo"


# 直接创建
class User(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.now)


# 创建引擎
engine = create_engine(db_url, echo=True)

# 创建table
SQLModel.metadata.create_all(engine)


# 插入数据
user = User(name="李四")
with Session(engine) as session:
    session.add(user)
    session.commit()

# 查询数据
with Session(engine) as session:
    entity = session.get(User, 1)
    print(entity)