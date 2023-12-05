import sys

sys.path.append(".")
from bot_admin.create_bot import bot, dp
from aiogram import types, Dispatcher
from .keyboards import get_admin_code, admin_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re
import random
from .models import Admin
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import MagicData


admin_router = Router()


class FSMadminauth(StatesGroup):
    email = State()
    code = State()


# class FSMadmincode(StatesGroup):
#     code = State()


@admin_router.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext):
    admin = ""
    async for adm in Admin.objects.filter(admin_telegram_id=message.from_user.id):
        if adm:
            admin = adm
    if admin:
        await bot.send_message(
            message.from_user.id,
            text="Ты попал в админ-панель!",
            reply_markup=admin_menu(),
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Пожалуйста, введи свою электронную почту, на которую"
            " тебя зарегистрировали в качестве администратора",
        )
        await state.set_state(FSMadminauth.email)


@admin_router.message(FSMadminauth.email)
async def fsm_admin_email(message: types.Message, state: FSMContext):
    if message.content_type == "text":
        admin = ""
        email = message.text
        await state.update_data(email=email)
        async for adm in Admin.objects.filter(email=email):
            if adm:
                admin = adm
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


@admin_router.callback_query(F.data == "email")
async def receive_code(callback: types.CallbackQuery, state: FSMContext):
    """Генерация рандомного кода и заведение его в БД"""
    code = random.randrange(1001, 9999)
    admin = ""
    admin_email = ""
    data = await state.get_data()
    print(data.values())
    async for adm in Admin.objects.filter(email=data["email"]):
        if adm:
            admin = adm
            admin.code = code
            await admin.asave()
            admin_email = adm.email
    if admin:
        send_mail(
            "Код",
            f"Твой код {code}",
            settings.EMAIL_HOST_USER,
            [admin_email],
            fail_silently=False,
        )
        await callback.message.edit_text(
            text="Напишите код из 4-х цифр, отправленнный на вашу почту"
        )
        await state.set_state(FSMadminauth.code)
        data = await state.get_data()
        await state.update_data(eee=code)
        print(data.values())
    else:
        await callback.message.edit_text(text="Ты не админ")


@admin_router.message(FSMadminauth.code)
async def fsm_admin_code(message: types.Message, state: FSMContext):
    """
    Админу присваивается телеграм айди при успешной проверке правильности введённого кода через FSM
    """
    if message.content_type == "text":
        code_status = False
        data = await state.get_data()
        data["eee"] = str(data["eee"])
        data["code"] = message.text
        if data["eee"] == message.text:
            async for adm in Admin.objects.filter(email=data["email"]):
                if adm:
                    adm.admin_telegram_id = message.from_user.id
                    await adm.asave()
                    code_status = True
                await state.clear()
        if code_status == True:
            await bot.send_message(
                message.from_user.id,
                text="Вы успешно авторизовались в админской части бота",
                reply_markup=admin_menu(),
            )


###LEGACY
# def register_handlers_admin(dp:Dispatcher):
#     dp.register_callback_query_handler(receive_code, text='email')
#     #dp.register_message_handler(admin_command, commands=["admin"])
#     dp.register_message_handler(
#         fsm_admin_email, content_types=["text"], state=FSMadminemail
#     )
#     dp.register_message_handler(fsm_admin_code, content_types=['text'],state=FSMadmincode)
