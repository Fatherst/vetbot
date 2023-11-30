import sys
sys.path.append(".")
from bot_admin.create_bot import bot,dp
from aiogram import types, Dispatcher
from .keyboards import (
    get_admin_code,
    admin_menu
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import random
from .models import Admin
import smtplib
from django.core.mail import send_mail
from django.conf import settings



class FSMadminemail(StatesGroup):
    email = State()


class FSMadmincode(StatesGroup):
    code = State()


async def admin_command(message: types.Message):
    admin = ''
    code = 0
    async for adm in Admin.objects.filter(admin_telegram_id=message.from_user.id):
        if adm:
            admin = adm
            code = adm.code
    if admin and code==1:
        await bot.send_message(message.from_user.id, text="Ты попал в админ-панель!", reply_markup=admin_menu())
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
        async with state.proxy() as data:
           data['email'] = message.text
           async for adm in Admin.objects.filter(email=data['email']):
               if adm:
                   admin = adm
                   await state.finish()
        if admin:
            admin.admin_telegram_id = message.from_user.id
            await admin.asave()
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
    admin = ''
    admin_email = ''
    async for adm in Admin.objects.filter(admin_telegram_id=callback.from_user.id):
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
        await FSMadmincode.code.set()
    else:
        await callback.message.edit_text(text='Ты не админ')

async def fsm_admin_code(message: types.Message,state: FSMContext):
    """Код должен измениться на 1 при успешном вводе, стать 0 при неудаче
    code_status временная переменная, чтобы в этой же функции проверить, прошёл ли админ проверку
    adm.code скорее всего можно не менять на 0 при неудаче, оставлять таким, как пришёл
    """
    if message.content_type == 'text':
        code_status = False
        async with state.proxy() as data:
           data['code'] = message.text
           async for adm in Admin.objects.filter(admin_telegram_id=message.from_user.id):
               if adm:
                   adm.code = str(adm.code)
                   if adm.code == data['code']:
                       adm.code = 1
                       await adm.asave()
                       code_status = True
                   else:
                       adm.code = 0
                       await adm.asave()
               await state.finish()
        if code_status == True:
            await bot.send_message(message.from_user.id, text='Вы успешно авторизовались в админской части бота',
                                   reply_markup=admin_menu())




def register_handlers_admin(dp:Dispatcher):
    dp.register_callback_query_handler(receive_code, text='email')
    dp.register_message_handler(admin_command, commands=["admin"])
    dp.register_message_handler(
        fsm_admin_email, content_types=["text"], state=FSMadminemail
    )
    dp.register_message_handler(fsm_admin_code, content_types=['text'],state=FSMadmincode)