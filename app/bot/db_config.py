from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import config

async_engine = create_async_engine(
    url=str(config.POSTGRES_URI),
    pool_size=1,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=600,
    pool_pre_ping=True,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
