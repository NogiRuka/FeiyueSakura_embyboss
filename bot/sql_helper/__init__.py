"""
初始化数据库 - 从MySQL改为SQLite
"""
import os
from bot import db_type, db_path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# 确保数据目录存在
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# 创建SQLite engine对象
if db_type == "sqlite":
    # SQLite数据库连接字符串
    database_url = f"sqlite:///{db_path}"
    engine = create_engine(
        database_url, 
        echo=False,  # 不显示SQL语句
        connect_args={"check_same_thread": False}  # SQLite多线程支持
    )
else:
    # 保留MySQL支持作为备选
    from bot import db_host, db_user, db_pwd, db_name, db_port
    database_url = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?utf8mb4"
    engine = create_engine(
        database_url, 
        echo=False,
        echo_pool=False,
        pool_size=16,
        pool_recycle=60 * 30,
    )

# 创建Base对象
Base = declarative_base()
Base.metadata.bind = engine
Base.metadata.create_all(bind=engine, checkfirst=True)


# 调用sql_start()函数，返回一个Session对象
def sql_start() -> scoped_session:
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


Session = sql_start()
