import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from src.db.types import Role

logger = logging.getLogger(__name__)


async def set_my_commands(bot: Bot, user_id: int, commands: list[BotCommand]) -> bool:
    try:
        await bot.delete_my_commands(BotCommandScopeChat(chat_id=user_id))
        return await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChat(chat_id=user_id),
        )
    except Exception as e:
        logger.error(f"Set commands for #{user_id} failed\n{e}")

    return False


async def set_default_commands(bot: Bot, user_id: int) -> bool:
    cmds = [BotCommand(command="start", description="Запустить бот")]
    return await set_my_commands(bot, user_id, cmds)
