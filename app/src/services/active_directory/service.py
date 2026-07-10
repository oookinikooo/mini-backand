from typing import Optional

from src.config import config

from .client import AsyncLDAP
from .exceptions import ProfileError
from .schemas import Profile


class Service:
    def __init__(self, attributes: Optional[list] = None):
        self._client = AsyncLDAP(server_url="corp.servolux.by",
                                 username=config.AD_LOGIN,
                                 password=config.AD_PASSWORD)
        self.attributes = attributes or ['*']

    async def search_by_id(self, user_id: int | str):
        resp = await self._client.search(
            search_base="dc=CORP,dc=SERVOLUX,dc=BY",
            search_filter=f"(extensionAttribute14={user_id})",
            attributes=self.attributes,
        )
        if resp:
            try:
                profile = Profile.model_validate(resp)
            except Exception as e:
                raise ProfileError(f"Invalid profile by ID {user_id}") from e
            return profile
        return None

    async def searcher_gen(self):
        async with self as client:
            user_id = yield
            while True:
                user_id = yield await client.search_by_id(user_id)

    async def close(self):
        await self._client.close()

    async def __aenter__(self) -> 'Service':
        if not self._client.conn or not self._client.conn.bound:
            await self._client.create_connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
