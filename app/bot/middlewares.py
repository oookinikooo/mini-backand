import logging
from collections.abc import Awaitable, Callable
from typing import Any, Dict, Union

from aiogram import BaseMiddleware
from aiogram.enums.chat_type import ChatType
from aiogram.types import CallbackQuery, Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.types import Status
from src.services.guest import GuestAdd, Guests
from src.services.user import Users

logger = logging.getLogger(__name__)


def is_private(obj: Message | CallbackQuery) -> bool:
    chat = obj.chat if isinstance(obj, Message) else obj.message.chat
    return chat.type == ChatType.PRIVATE


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker: AsyncSession):
        self.session_maker = session_maker

    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with self.session_maker() as session:
            data["session"] = session
            return await handler(event, data)


class IndentifyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        if not is_private(event):
            return

        session = data["session"]

        user_id = event.from_user.id
        users = Users(session)
        if user := await users.get(user_id):
            if user.status != Status.ACTIVE:
                return

            data["user"] = user
            return await handler(event, data)

        guests = Guests(session)
        guest = await guests.get(user_id)
        if not guest:
            unknown_user = GuestAdd(id=user_id, full_name=event.from_user.full_name)
            added_id = await guests.register(unknown_user)

            logger.info(
                f"Register guest {unknown_user.full_name!r} (#{user_id}). "
                f"Ok: {bool(added_id)}"
            )
            guest = await guests.get(user_id)

        if guest and guest.status == Status.ACTIVE:
            data["guest"] = guest
            return await handler(event, data)
