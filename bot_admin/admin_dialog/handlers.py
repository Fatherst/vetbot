import sys
sys.path.append(".")
from bot_admin.create_bot import bot,dp
from aiogram import types, Dispatcher
from .keyboards import (
    get_admin_code,
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import random



class FSMadminemail(StatesGroup):
    email = State()


class FSMadmincode(StatesGroup):
    code = State()


async def admin_command(message: types.Message):
    if "user.tg_id" in "table_admins":
        await bot.send_message(message.from_user.id, text="Ты попал в админ-панель!")
    else:
        await bot.send_message(
            message.from_user.id,
            text="Пожалуйста, введи свою электронную почту, на которую"
            " тебя зарегистрировали в качестве администратора",
        )
        await FSMadminemail.email.set()


async def fsm_admin_email(message: types.Message, state: FSMContext):
    if message.content_type == "text":
        admin = ""
        # async with state.proxy() as data:
        #    data['email'] = message.text
        #    async for adm in 'Admin.objects.filter(email=data[email])':
        #        if adm:
        #            admin = adm
        if admin:
            await bot.send_message(
                message.from_user.id,
                text="Вы найдены в базе данных администраторов\n"
                "После нажатия кнопки на вашу почту придёт код,"
                "который надо будет написать после нажатия кнопки",
                reply_markup=get_admin_code(),
            )
        else:
            await bot.send_message(
                message.from_user.id, text="Вы не найдены в базе администраторов"
            )


async def receive_code(callback: types.CallbackQuery):
    """Генерация рандомного кода и заведение его в БД"""
    code = random.randrange(1001, 9999)
    """
    admin = Admin.objects.filter(telegramid=callback.from_user.id)
    admin.code = code
    """
    # send_code
    await callback.message.edit_text(
        text="Напишите код из 4-х цифр, отправленнный на вашу почту"
    )
    await FSMadmincode.code.set()


def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(admin_command, commands=["admin"])
    dp.register_message_handler(
        fsm_admin_email, content_types=["text"], state=FSMadminemail
    )