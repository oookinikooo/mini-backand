from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
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
AsyncSessionMaker: AsyncSession = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


async def get_session():
    async with AsyncSessionMaker() as session:
        yield session


async def init_db():
    from .models import Base, User

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
