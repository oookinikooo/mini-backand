from abc import ABC

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class DefaultRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar()

    async def select_one(self, id: int):
        query = select(self.model).filter(self.model.id == id)
        resp = await self.session.execute(query)
        return resp.scalar()

    async def update_one(self, id: int, data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        updated_row = await self.session.execute(stmt)
        await self.session.commit()
        return updated_row.scalar()

    async def delete(self, id: int) -> int | None:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        resp = await self.session.execute(stmt)
        await self.session.commit()
        return resp.scalar()
