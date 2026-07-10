from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import (
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from src.db.models import User

from .filters import IsUser

MINI_APP_URL = "https://dev-app-87355.firebaseapp.com/"

def mini_app_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [IButton(text="🚀 Open app", web_app=WebAppInfo(url=MINI_APP_URL))]
    ])


async def cmd_start(message: Message, user: User):
    await message.answer(f"Hi {user.name_pretty}", reply_markup=mini_app_kb())


def attach(dp: Dispatcher):
    router = Router()
    router.message.register(cmd_start, Command("start"), IsUser())
    dp.include_router(router)
