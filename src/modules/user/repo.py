from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.core.db import DefaultRepository


class Repository(DefaultRepository):
    model = User

    # async def add(self, data: dict):

    # async def select_where_user(self, user_id: int):
    #     query = select(self.model).where(self.model.user_id == user_id)
    #     resp = await self.session.execute(query)
    #     return resp.scalars().all()
