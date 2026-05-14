from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from .repo import Repository
from .schemas import UserAdd


class Service:
    def __init__(self, session: AsyncSession):
        self._repo = Repository(session)

    async def register(self, user: UserAdd) -> User | None:
        return await self._repo.add(user.model_dump())

    async def get(self, user_id: int | str) -> User | None:
        if isinstance(user_id, str) and not user_id.isdigit():
            return None
        return await self._repo.get(int(user_id))
