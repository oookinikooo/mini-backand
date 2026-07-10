from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import DefaultRepository
from src.db.models import User


class Repository(DefaultRepository):
    model = User

    # async def add(self, data: dict):

    # async def select_where_user(self, user_id: int):
    #     query = select(self.model).where(self.model.user_id == user_id)
    #     resp = await self.session.execute(query)
    #     return resp.scalars().all()

    async def select_where_login(self, login: str) -> User | None:
        query = select(self.model).filter(self.model.login == login)
        resp = await self.session.execute(query)
        return resp.scalar()
