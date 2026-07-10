import logging
from datetime import datetime

from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
from aiogram.types import InlineKeyboardButton as IButton
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Guest
from src.db.types import Status
from src.services.active_directory import Profile, ProfileError, Profiles
from src.services.guest import Guests
from src.services.user import Users

from .commands import set_default_commands
from .db_config import AsyncSessionLocal
from .filters import IsGuest

logger = logging.getLogger()

MINI_APP_URL = "https://dev-app-87355.firebaseapp.com/"


def has_not_access_yet(total_attempts: int):
    return (
        "⚠️ <b>У Вас нет доступа к боту</b>\n\n"
        f"Количетсво оставшихся попыток авторизации: {total_attempts}\n\n"
        "<i>Примечание: Для получения доступа пройдите регистрацию "
        "в @servolux_bot и получите необходимые права для пользования "
        "данным ботом</i>"
    )


def change_account(old_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [IButton(text="Сменить аккаунт", callback_data=f"{old_id}~change_account")],
            [IButton(text="Отменить", callback_data="~change_account")],
        ]
    )


def mini_app_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [IButton(text="🚀 Open app", web_app=WebAppInfo(url=MINI_APP_URL))]
        ]
    )


def auth_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                IButton(text="Login", callback_data="~check_access"),
            ]
        ]
    )


async def cmd_start(message: Message, guest: Guest, session: AsyncSession):
    if not guest.welcomed:

        await message.bot.set_chat_menu_button(
            guest.id, None
        )


        guest.welcomed = True
        try:
            await session.commit()
        except Exception as e:
            logger.error(f"Change welcomed flag for #{guest.id} failed - {e}")

        await set_default_commands(message.bot, guest.id)

        await message.answer(
            "Добро пожаловать в бот «[Name]»\n"
            "Воспользуйтесь кнопкой ниже, чтобы начать работу",
            reply_markup=auth_kb(),
        )
    else:
        await message.answer(
            has_not_access_yet(guest.total_attempts),
            reply_markup=auth_kb(),
        )


def have_to_wait(until: datetime) -> str | None:
    seconds = (until - datetime.now()).total_seconds()
    if seconds > 0.0:
        h, m = divmod(seconds, 3600)
        m, s = divmod(m, 60)
        return f"Время ожидания: {int(h):02}:{int(m):02}:{int(s):02}"
    return None


def failed_reason(profile: Profile | None):
    if not profile:
        return (
            "⚠️ <b>Пользовательский профиль не найден</b>\n\n"
            "<i>Примечание: Пройдите регистрацию в @servolux_bot и "
            "получите необходимые права для пользования ботом</i>"
        )

    elif not profile.is_active:
        return "⚠️ Пользовательский профиль заблокирован"

    elif profile.is_active and not profile.has_access:
        return (
            "⚠️ <b>У Вас нет прав на доступ к боту</b>\n\n"
            "<i>Примечание: Для получения прав воспользуйтесь @servolux_bot</i>"
        )

    else:
        return (
            "Пользовательский профиль существует и обладает необходимыми правами на бот"
        )


async def cb_check_access(cb: CallbackQuery, guest: Guest, session: AsyncSession):
    if guest.is_frozen and (text := have_to_wait(guest.frozen_until)):
        await cb.answer(text, show_alert=True)
        return

    await cb.answer()

    waiting = await cb.message.edit_text(
        "Проводиться проверка наличия необходимых прав для работы с ботом. Ожидайте..."
    )
    await session.close()
    try:
        profile = Profile(
            id=guest.id,
            firstname="Nikolay",
            login="some.some",
            is_active=True,
            middle_name="Andreevich",
            surname="Adamov",
        )
        profile.is_active = False
        # async with Profiles() as service:
        #     profile: Profile | None = await service.search_by_id(guest.id)
    except Exception as e:
        if isinstance(e, ProfileError):
            logger.error(f"{type(e).__name__}: {e}, 'cause {e.__cause__}")
            # await chat_logger.error(f"Invalid AD-profile for user:{guest.id}")
        else:
            logger.error(f"Get AD profile failed\n{type(e).__name__}: {e}")

        await waiting.edit_text(
            "❌ Сервис для проверки учетных данных временно "
            "недоступен.\n\nПовторите попытку позже!",
            reply_markup=auth_kb(),
        )
        return

    async with AsyncSessionLocal() as session:
        if profile and not profile.is_active:
            guest.status = Status.BLOCKED
            await session.commit()

            logger.info(f"Block user #{guest.id}, 'cause inactive AD profile")
            await waiting.edit_text(
                "❌ <b>Вы заблокированны</b>\n\n<i>Профиль пользователя в "
                "учетной системе заблокирован</i>"
            )
            return

        if profile and profile.has_access:
            if user := await Users(session).get_by_login(profile.login):
                await waiting.edit_text(
                    "⚠️ <b>Дублирование аккаунтов</b>\n\n"
                    f"Аккаунт с логином {user.login} уже существует и принадлежит "
                    f"пользователю {user.full_name}, если это Вы и хотите работать "
                    "с ботом под другим аккаунтом нажмите кнопку Сменить аккаунт\n",
                    reply_markup=change_account(user.id),
                )
                return

            await Users(session).register_from_profile(profile)

            removed_id = await Guests(session).remove(guest.id)

            logger.info(
                f"Login user #{guest.id} - {profile.surname!r} (remove tmp: {bool(removed_id)})"
            )
            # await chat_logger.info(f"Login {profile.full_name!r} (#{guest.id})")

            await waiting.edit_text(
                "✅ Доступ предоставлен!\n\n"
                "Данный бот создан для [...]\n"
                "Открывааааай",
                reply_markup=mini_app_kb(),
            )

            await cb.bot.set_chat_menu_button(
                guest.id,
                MenuButtonWebApp(text="Open", web_app=WebAppInfo(url=MINI_APP_URL)),
            )
            return

        if not profile:
            text = (
                "⚠️ <b>Пользовательский профиль не найден</b>\n\n"
                "<i>Примечание: Пройдите регистрацию в @servolux_bot и "
                "получите необходимые права для пользования ботом</i>"
            )
        else:
        # elif profile.is_active and not profile.has_access:
            text = (
                "⚠️ <b>У Вас нет прав на доступ к боту</b>\n\n"
                "<i>Примечание: Для получения прав воспользуйтесь @servolux_bot</i>"
            )

        await waiting.edit_text(text)
        # await waiting.edit_text(failed_reason(profile))

        guest.total_attempts -= 1
        if guest.total_attempts > 0:
            await Guests(session).freeze(guest.id)
            text, rpm = has_not_access_yet(guest.total_attempts), auth_kb()
        else:
            guest.status = Status.BLOCKED

            logger.info(f"User #{guest.id} blocked, 'cause spent attempts")
            text = (
                "❗️ <b>Вы заблокированы</b>\n\nЗакончились попытки отведенные "
                "на авторизацию"
            )
            rpm = None

        try:
            await session.commit()
        except Exception as e:
            print(f"fuck: {e}")

    await waiting.answer(text, reply_markup=rpm)



async def cb_change_account(cb: CallbackQuery, guest: Guest, session: AsyncSession):
    await cb.answer()

    prev_id, *_ = cb.data.split("~")
    if not prev_id.isdigit():
        removed_id = await Guests(session).remove(guest.id)

        await cb.message.edit_text("Действие по смене аккаунта отменено")
        return

    prev_id = int(prev_id)
    is_ok = await Users(session).change_account_id(prev_id, guest.id)
    if not is_ok:
        await cb.message.edit_text(
            "⚠️ <b>Ошибка смены аккаунта</b>\n\nПовторите попытку...",
            reply_markup=change_account(prev_id),
        )
        return

    removed_id = await Guests(session).remove(guest.id)

    await cb.message.edit_text(
        f"Смена аккаунта c <code>{prev_id}</code> на "
        f"<code>{guest.id}</code> успешно завершена\n\n"
        "Нажмите на кнопку ниже чтобы начать работу",
        reply_markup=mini_app_kb(),
    )

    await cb.bot.set_chat_menu_button(
        guest.id,
        MenuButtonWebApp(text="Open", web_app=WebAppInfo(url=MINI_APP_URL)),
    )

    logger.info(
        f"User #{prev_id} relogin with #{guest.id}. Ok: {is_ok}. "
        f"Remove tmp: {bool(removed_id)}"
    )
    # await chat_logger.info(
    #     f"User Relogin from #{prev_id} to #{prev_id} "
    #     f"(is_ok: {is_ok}, del tmp: {bool(removed_id)})"
    # )


def attach(dp: Dispatcher):
    router = Router()
    router.message.register(cmd_start, Command("start"), IsGuest())
    router.callback_query.register(
        cb_check_access, F.data.endswith("~check_access"), IsGuest()
    )
    router.callback_query.register(
        cb_change_account, F.data.endswith("~change_account"), IsGuest()
    )

    dp.include_router(router)
