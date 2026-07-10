import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from src.config import config

from . import logged, sign_up
from .db_config import AsyncSessionLocal, async_engine
from .middlewares import DBSessionMiddleware, IndentifyMiddleware

logging.basicConfig(
    level="INFO",
    format="%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("some")


async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.update.middleware(DBSessionMiddleware(AsyncSessionLocal))
    dp.message.outer_middleware(IndentifyMiddleware())
    dp.callback_query.outer_middleware(IndentifyMiddleware())

    sign_up.attach(dp)
    logged.attach(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    async with bot:
        await dp.start_polling(bot, polling_timeout=60)


if __name__ == "__main__":
    asyncio.run(main())
