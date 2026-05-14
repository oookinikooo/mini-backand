from abc import ABC

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.core.config import config

async_engine = create_async_engine(url=str(config.POSTGRES_URI), echo=False)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session():
    async with async_session_maker() as session:
        yield session


async def init_db():
    from src.models.base import Base
    from src.models.user import User

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class DefaultRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar()

    async def get(self, id: int):
        query = select(self.model).filter(self.model.id == id)
        resp = await self.session.execute(query)
        return resp.scalar_one_or_none()

    async def update(self, id: int, data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
        )
        updated_row = await self.session.execute(stmt)
        await self.session.commit()
        return updated_row.scalar_one_or_none()

    async def delete(self, id: int) -> int | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model.id)
        )
        resp = await self.session.execute(stmt)
        await self.session.commit()
        return resp.scalar_one_or_none()
