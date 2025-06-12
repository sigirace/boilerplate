from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from configs import get_settings


setting = get_settings()
DATABASE_URL = setting.mysql.async_url()

# 비동기 엔진
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

Base = declarative_base()
