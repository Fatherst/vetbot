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


class FSMadminauth(StatesGroup):
    email = State()
    code = State()


@admin_router.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext, bot: Bot):
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
        await state.set_state(FSMadminauth.email)


@admin_router.message(FSMadminauth.email)
async def fsm_admin_email(message: types.Message, state: FSMContext, bot: Bot):
    if message.content_type == "text":
        email = message.text
        await state.update_data(email=email)
        admin = await Admin.objects.filter(email=email).afirst()
        if admin:
            code = random.randrange(1001, 9999)
            await bot.send_message(
                message.from_user.id,
                text="Вы найдены в базе данных администраторов\n"
                "На вашу почту отправлен код,"
                " напишите его здесь",
            )
            await state.set_state(FSMadminauth.code)
            await state.update_data(code=code)
            data = await state.get_data()
            print(data)
        else:
            await bot.send_message(
                message.from_user.id, text="Вы не найдены в базе администраторов"
            )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Пожалуйста, пришли свою электронную почту текстом",
        )


@admin_router.message(FSMadminauth.code)
async def fsm_admin_code(message: types.Message, state: FSMContext, bot: Bot):
    """
    Админу присваивается телеграм айди при успешной проверке правильности введённого кода через FSM
    """
    if message.content_type == "text":
        data = await state.get_data()
        data["code"] = str(data["code"])
        if data["code"] == message.text:
            admin = await Admin.objects.filter(email=data["email"]).afirst()
            admin.tg_chat_id = message.from_user.id
            await admin.asave()
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
