from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import Account
from src.core.db import DefaultRepository


class Repository(DefaultRepository):
    model = Account

    async def add(self, data: dict) -> Account | None:
        return await super().add(data)

    async def select_where_user(self, user_id: int):
        query = select(self.model).where(self.model.user_id == user_id)
        resp = await self.session.execute(query)
        return resp.scalars().all()
