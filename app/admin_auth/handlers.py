from aiogram import types
from django.core.mail import send_mail
from django.conf import settings
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import random
from .models import Admin
from .keyboards import admin_menu



admin_router = Router()


class AdminAuthStates(StatesGroup):
    email = State()
    code = State()


@admin_router.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext):
    await state.clear()
    admin = await Admin.objects.filter(tg_chat_id=message.from_user.id).afirst()
    if admin:
        await message.answer(
            text="Ты попал в админ-панель!",
            reply_markup=admin_menu(),
        )
    else:
        await message.answer(
            text="Пожалуйста, введи свою электронную почту, на которую"
            " тебя зарегистрировали в качестве администратора",
        )
        await state.set_state(AdminAuthStates.email)


@admin_router.message(AdminAuthStates.email)
async def handle_admin_email(message: types.Message, state: FSMContext):
    """Тут и в клиентской части код пока что просто 1"""
    email = message.text
    await state.update_data(email=email)
    admin = await Admin.objects.filter(email=email).afirst()
    if admin:
        code = random.randrange(1001, 9999)
        await message.answer(
            text="Вы найдены в базе данных администраторов\n"
            "На вашу почту отправлен код,"
            " напишите его здесь",
        )
        await state.set_state(AdminAuthStates.code)
        await state.update_data(code=code)
        send_mail(
            "Код",
            f"Ваш код {code}",
            settings.EMAIL_HOST_USER,
            [f"{email}"],
            fail_silently=False,
        )
    else:
        await message.answer(text="Вы не найдены в базе администраторов")


@admin_router.message(AdminAuthStates.code)
async def handle_admin_email_code(message: types.Message, state: FSMContext):
    """
    Админу присваивается телеграм айди при успешной проверке правильности введённого кода через FSM
    """
    data = await state.get_data()
    if str(data["code"]) == message.text:
        await Admin.objects.filter(email=data["email"]).aupdate(
            tg_chat_id=message.from_user.id
        )
        await state.clear()
        await message.answer(
            text="Вы успешно авторизовались в админской части бота",
            reply_markup=admin_menu(),
        )
    else:
        await message.answer(
            text="Код неправильный, попробуйте ещё раз или нажмите /admin, чтобы начать сначала",
        )
