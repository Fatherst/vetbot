from aiogram import types
from .keyboards import admin_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import random
from .models import Admin
from django.core.mail import send_mail
from django.conf import settings
from aiogram import Router, F
from aiogram.filters import Command
from aiogram import Bot


admin_router = Router()


class AdminAuthStates(StatesGroup):
    email = State()
    code = State()


@admin_router.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    admin = await Admin.objects.filter(tg_chat_id=message.from_user.id).afirst()
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
        await state.set_state(AdminAuthStates.email)


@admin_router.message(AdminAuthStates.email)
async def recieve_admin_email(message: types.Message, state: FSMContext, bot: Bot):
    """Тут и в клиентской части код пока что просто 1"""
    email = message.text
    await state.update_data(email=email)
    admin = await Admin.objects.filter(email=email).afirst()
    if admin:
        # code = random.randrange(1001, 9999)
        code = 1
        await bot.send_message(
            message.from_user.id,
            text="Вы найдены в базе данных администраторов\n"
            "На вашу почту отправлен код,"
            " напишите его здесь",
        )
        await state.set_state(AdminAuthStates.code)
        await state.update_data(code=code)
    else:
        await bot.send_message(
            message.from_user.id, text="Вы не найдены в базе администраторов"
        )


@admin_router.message(AdminAuthStates.code)
async def recieve_admin_email_code(message: types.Message, state: FSMContext, bot: Bot):
    """
    Админу присваивается телеграм айди при успешной проверке правильности введённого кода через FSM
    """
    data = await state.get_data()
    if str(data["code"]) == message.text:
        await Admin.objects.filter(email=data["email"]).aupdate(
            tg_chat_id=message.from_user.id
        )
        await state.clear()
        await bot.send_message(
            message.from_user.id,
            text="Вы успешно авторизовались в админской части бота",
            reply_markup=admin_menu(),
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Код неправильный, попробуйте ещё раз или нажмите /admin, чтобы начать сначала",
        )
