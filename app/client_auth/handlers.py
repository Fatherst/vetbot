from aiogram import types
from .keyboards import (
    get_contact,
    get_user_received_from_db,
)
from aiogram import Bot
from .models import Client
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import Command, and_f
import re
import random


client_router = Router()


class FSMPhone(StatesGroup):
    phone = State()
    code = State()


@client_router.message(Command("start"))
async def command_start(message: types.Message, bot: Bot, state: FSMContext):
    """
    Проверка на то, зарегистрирован ли пользователь уже
    """
    user_id = message.from_user.id
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    if client:
        await bot.send_message(
            message.from_user.id,
            text=f"*{client.first_name}*, приветствую!\n\nВыберите, что вас интересует ⤵",
            reply_markup=get_user_received_from_db(),
            parse_mode="Markdown",
        )
    else:
        greeting = (
            "Добро пожаловать в бота ветеринарного центра *Друзья* 🐈\n"
            "Для начала мне нужно Вас идентифицировать в качестве клиента нашей клиники. "
            "Для этого,пожалуйста,нажмите на кнопку чтобы отправить свой номер телефона,"
            " указанный в Telegram, или напишите его вручную"
        )
        await bot.send_message(
            message.from_user.id,
            text=greeting,
            reply_markup=get_contact(),
            parse_mode="Markdown",
        )
        await state.set_state(FSMPhone.phone)


@client_router.message(FSMPhone.phone, and_f(F.text))
async def fsm_number_get(message: types.Message, state: FSMContext, bot: Bot):
    code = 1
    # code = random.randrange(1001, 9999)
    black_list = []
    if re.match("[+]+?[7](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})", f"{message.text}"):
        await bot.send_message(
            message.from_user.id,
            text="Спасибо! Проверяем вас в базе данных",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        user_phone_number = message.text
        client = await Client.objects.filter(phone_number=user_phone_number).afirst()
        if client and client not in black_list:
            await state.update_data(code=code)
            await state.update_data(phone_number=user_phone_number)
            await bot.send_message(
                message.from_user.id,
                text=f"*{client.first_name}*, приветствую!\n\n"
                f"Напишите код из 4-х цифр, который придёт на ваш телефон",
                parse_mode="Markdown",
            )
            await state.set_state(FSMPhone.code)
        elif client in black_list:
            await bot.send_message(
                message.from_user.id,
                text="Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна.",
            )
        else:
            client = await Client.objects.acreate(
                phone_number=user_phone_number, first_name=message.from_user.first_name
            )
            await client.asave()
            await state.update_data(code=code)
            await state.update_data(phone_number=user_phone_number)
            await bot.send_message(
                message.from_user.id,
                text=f"*{client.first_name}*, приветствую!\n\n"
                f"Напишите код из 4-х цифр, который придёт на ваш телефон",
                parse_mode="Markdown",
            )
            await state.set_state(FSMPhone.code)
    elif message.text.lower() == "отмена":
        await state.clear()
        await bot.send_message(message.from_user.id, text="Возврат в меню")
    elif not re.match("[+]+?[7](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})", f"{message.text}"):
        await message.reply(
            text='Номер должен быть в формате +7XXXXXXXXXX\nПопробуй ещё раз или напиши "Отмена", либо /start'
        )


@client_router.message(FSMPhone.phone, and_f(F.content_type.in_({"contact"})))
async def recieve_contact(message: types.Message, bot: Bot, state: FSMContext):
    code = 1
    black_list = []
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await bot.send_message(
        message.from_user.id, text="Спасибо! Проверяем вас в базе данных"
    )
    client = await Client.objects.filter(phone_number=phone_number).afirst()
    if client and client not in black_list:
        await state.update_data(code=code)
        await state.update_data(phone_number=phone_number)
        await bot.send_message(
            message.from_user.id,
            text=f"*{client.first_name}*, приветствую!\n\n"
            f"Напишите код из 4-х цифр, который придёт на ваш телефон",
            parse_mode="Markdown",
        )
        await state.set_state(FSMPhone.code)
    elif client in black_list:
        await bot.send_message(
            message.from_user.id,
            text="Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна.",
        )
    else:
        client = await Client.objects.acreate(
            phone_number=phone_number, first_name=message.from_user.first_name
        )
        await client.asave()
        await state.update_data(code=code)
        await state.update_data(phone_number=phone_number)
        await bot.send_message(
            message.from_user.id,
            text=f"*{client.first_name}*, приветствую!\n\n"
            f"Напишите код из 4-х цифр, который придёт на ваш телефон",
            parse_mode="Markdown",
        )
        await state.set_state(FSMPhone.code)


@client_router.message(FSMPhone.code)
async def fsm_receive_code(message: types.Message, state: FSMContext, bot: Bot):
    if message.content_type == "text":
        data = await state.get_data()
        data["code"] = str(data["code"])
        if data["code"] == message.text:
            client = await Client.objects.filter(
                phone_number=data["phone_number"]
            ).afirst()
            client.tg_chat_id = message.from_user.id
            await client.asave()
            await state.clear()
            await bot.send_message(
                message.from_user.id,
                text="Вы успешно авторизовались в клиентской части бота",
                reply_markup=get_user_received_from_db(),
            )
        elif data["code"] != message.text:
            await bot.send_message(
                message.from_user.id,
                text="Код неправильный, попробуй ввести ещё раз, либо напиши 'Отмена' или /start, чтобы начать сначала",
            )
        elif message.text.lower() == "Отмена":
            await bot.send_message(
                message.from_user.id, text="Нажмите /start, чтобы начать сначала"
            )
            await state.clear()
    else:
        await bot.send_message(
            message.from_user.id, text="Пожалуйста, пришлите код текстом"
        )
