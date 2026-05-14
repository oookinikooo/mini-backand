from typing import Sequence

from src.models.account import Account
from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from .schemas import AccountAdd


class Service:
    def __init__(self, session: AsyncSession):
        self._repo = Repository(session)

    async def create(self, data: AccountAdd) -> Account | None:
        return await self._repo.add(data.model_dump())

    async def get_by_user(self, user_id: int) -> Sequence[Account]:
        return await self._repo.select_where_user(user_id)
