import logging
from collections.abc import Sequence
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Guest
from src.db.types import Status

from .repo import Repository
from .schema import GuestAdd

logger = logging.getLogger("service.auth")


class Service:
    def __init__(self, session: AsyncSession):
        self._repo = Repository(session)

    async def _add(self, data: dict) -> int | None:
        return await self._repo.insert_one(data)

    async def register(self, user: GuestAdd) -> int | None:
        return await self._add(user.model_dump())

    async def remove(self, user_id: int) -> int | None:
        return await self._repo.delete(user_id)

    async def _update(self, id: int, data: dict) -> Guest | None:
        return await self._repo.update_one(id, data)

    async def get(self, user_id: int | str) -> Guest | None:
        if isinstance(user_id, str) and not user_id.isdigit():
            raise ValueError("User_id must be int")

        if row := await self._repo.select_one(int(user_id)):
            return row
        return None

    async def add_more_attempts(self, user_id: int, count: int = 3) -> bool | None:
        user = await self.get(user_id)
        if user:
            data = {
                "total_attempts": count,
                "frozen_until": None,
                "status": Status.ACTIVE,
            }
            updated = await self._update(user_id, data)
            return bool(updated)
        return None

    async def freeze(self, user_id: int):
        user = await self.get(user_id)
        if user:
            a = user.total_attempts  # 3, 2, 1, 0
            if a > 0:
                position = 3 if a > 3 else a
                t = [15, 10, 5][position - 1]
                until = datetime.now() + timedelta(minutes=t)
                await self._update(user_id, {"frozen_until": until})

    async def get_count(self, status: Status | None = None) -> int:
        resp = await self._repo.select_count(status)
        return resp if resp else 0

    async def get_by_page(
        self, page: int, cap: int = 5, *, status: Status | None = None
    ) -> Sequence[Guest]:
        offset = 0 if page == 0 else page * cap
        return await self._repo.select_slice(cap, offset, status)

    # async def welcomed(self, user_id: int):
    #     resp = await self._update(user_id, {"welcomed": True})
    #     return bool(resp)

    # async def set_status(self, user_id: int, value: Status):
    #     resp = await self._update(user_id, {"status": value})
    #     return bool(resp)

    # async def fault(self, user_id: int) -> int | None:
    #     if user := await self.get(user_id):
    #         rest_attempts = user.total_attempts - 1
    #         data = {"total_attempts": rest_attempts}
    #         if rest_attempts == 0:
    #             data.update({"status": Status.BLOCKED})

    #         await self._update(user_id, data)
    #         return rest_attempts
    #     return None