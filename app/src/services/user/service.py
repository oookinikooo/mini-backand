from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User as UserRaw
from src.db.types import Status
from src.services.active_directory import Profile

from .repo import Repository
from .schemas import User, UserAdd


class Service:
    def __init__(self, session: AsyncSession):
        self._repo = Repository(session)

    def to_model(self, user: UserRaw | None) -> User | None:
        if user:
            return User.model_validate(user)
        return None

    async def register(self, user: UserAdd) -> User | None:
        resp = await self._repo.insert_one(user.model_dump())
        return self.to_model(resp)

    async def get(self, user_id: int | str) -> User | None:
        if isinstance(user_id, str) and not user_id.isdigit():
            return None
        resp = await self._repo.select_one(int(user_id))
        return self.to_model(resp)

    async def _update(self, id: int, data: dict) -> User | None:
        return await self._repo.update_one(id, data)

    async def register_from_profile(self, profile: Profile) -> int | None:
        return await self.register(
            UserAdd(
                id=profile.id,
                login=profile.login,
                firstname=profile.firstname,
                middle_name=profile.middle_name,
                surname=profile.surname,
            )
        )

    # async def get_by_page(
    #     self, page: int, cap: int = 5, status: Status = Status.ACTIVE
    # ) -> Sequence[User]:
    #     offset = 0 if page == 0 else page * cap
    #     return await self._repo.select_by_filter(cap, offset, status)

    # async def row_generator(self) -> AsyncGenerator[User, None]:
    #     p = 0
    #     while True:
    #         if users := await self.get_by_page(p, cap=20):
    #             for u in users:
    #                 yield u

    #             p += 1
    #         else:
    #             break

    async def get_by_login(self, login: str) -> User | None:
        resp = await self._repo.select_where_login(login)
        return self.to_model(resp)

    async def change_account_id(self, current_id: int, new_id: int) -> bool:
        updated = await self._update(current_id, {"id": new_id, "status": Status.ACTIVE})
        return bool(updated)