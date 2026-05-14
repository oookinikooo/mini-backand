import asyncio

from ldap3 import ALL, Connection, Entry, Server


class AsyncLDAP:
    def __init__(
        self,
        server_url: str,
        username: str,
        password: str,
        timeout: int = 10,
    ):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.conn = None

    async def create_connection(self) -> bool:
        self.conn = await asyncio.to_thread(
            lambda: Connection(
                Server(self.server_url, get_info=ALL, connect_timeout=self.timeout),
                user=self.username,
                password=self.password,
                auto_bind=True,
                raise_exceptions=True,
            )
        )
        return self.conn.bound

    async def close(self) -> None:
        if self.conn:
            await asyncio.to_thread(self.conn.unbind)

    async def search(
        self, search_base: str, search_filter: str, attributes: list = None
    ) -> dict:
        if not self.conn or not self.conn.bound:
            await self.create_connection()

        await asyncio.to_thread(
            lambda: self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                attributes=attributes or ['*']
            )
        )
        return self.entries2dict()

    def entries2dict(self) -> dict:
        converted_data = {}
        if (entries := self.conn.entries) and entries[0]:
            entry: Entry = entries[0]
            for k, value in entry.entry_attributes_as_dict.items():
                if isinstance(value, list):
                    if not value:
                        value = None
                    elif len(value) == 1:
                        if isinstance(value[0], str):
                            value = value[0].strip()
                        else:
                            value = value[0]
                converted_data[k] = value
