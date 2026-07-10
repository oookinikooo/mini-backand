from aiogram.filters import BaseFilter
from src.db.models import Guest, User
from src.db.types import Role


class IsGuest(BaseFilter):
    async def __call__(self, obj, guest: Guest | None = None) -> bool:
        return bool(guest)


class RoleFilter(BaseFilter):
    def __init__(self, role: Role):
        self.role = role

    async def __call__(self, obj, user: User | None = None) -> bool:
        return bool(user and user.role == self.role)


class IsUser(RoleFilter):
    def __init__(self):
        super().__init__(Role.USER)


class IsManager(RoleFilter):
    def __init__(self):
        super().__init__(Role.MANAGER)


class IsLogged(BaseFilter):
    async def __call__(self, obj, user: User) -> bool:
        return bool(user)
