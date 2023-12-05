import sys

sys.path.append(".")
from aiogram import types, Dispatcher
from .keyboards import (
    get_identification,
    get_contact,
    get_user_received_from_db,
    get_user_not_in_db,
    get_new_appointment,
)
from .models import Client
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_admin.create_bot import bot, dp
from aiogram import Router, F
from aiogram.filters import Command
import re


client_router = Router()


class FSMPhone(StatesGroup):
    phone = State()


@client_router.message(Command("start"))
async def command_start(message: types.Message):
    """Проверка, является ли пользователь администратором, надо реализовать админку
    Проверка на то, зарегистрирован ли пользователь уже"""
    user_id = message.from_user.id
    user = ""
    """async надо делать, потому что по-другому ORM не работает(потому что она синхронная по умолчанию)"""
    async for client in Client.objects.filter(client_telegram_id=user_id):
        if client:
            user = client
    if user:
        await bot.send_message(
            message.from_user.id,
            text=f"*{user.first_name}*, приветствую!\n\nВыберите, что вас интересует ⤵",
            reply_markup=get_user_received_from_db(),
            parse_mode="Markdown",
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Добро пожаловать в бота ветеринарного центра *Друзья* 🐈\nДля начала мне нужно Вас идентифицировать в качестве клиента нашей клиники. Для этого,пожалуйста, выберите, хотите"
            "ли вы отправить свой номер телефона, указанный в Telegram или написать его вручную.",
            reply_markup=get_identification(),
            parse_mode="Markdown",
        )


# @client_router.callback_query(F.data=='1')
# async def identification(callback: types.CallbackQuery):
#     await callback.message.edit_text(
#         text="Вы хотите поделиться свои номером телефона этому боту"
#         " или прислать номер телефона сообщением?",
#         reply_markup=get_identification(),
#     )


@client_router.callback_query(F.data == "write")
async def fsm_number(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Пожалуйста, напишите свой телефон в формате: +7XXXXXXXXX"
    )
    await state.set_state(FSMPhone.phone)


@client_router.message(FSMPhone.phone)
async def fsm_number_get(message: types.Message, state: FSMContext):
    if message.content_type == "text" and re.match(
        "[+]+?[7](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})", f"{message.text}"
    ):
        user_telegram_id = message.from_user.id
        user = ""
        data = await state.get_data()
        phone = message.text
        data["phone"] = phone
        """Функция дублирует такую же в number_received"""
        async for client in Client.objects.filter(phone_number=phone):
            if client:
                user = client
                client.client_telegram_id = user_telegram_id
                await client.asave()
        await state.clear()
        black_list = []
        if user and user not in black_list:
            await bot.send_message(
                message.from_user.id,
                text=f"*{user.first_name}*, приветствую!\n\nВыберите, что вас интересует ⤵️",
                parse_mode="Markdown",
                reply_markup=get_user_received_from_db(),
            )
        elif user and user in black_list:
            await bot.send_message(
                message.from_user.id,
                text="Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна.",
            )
        elif not user:
            await bot.send_message(
                message.from_user.id,
                text="К сожалению, я не смог найти Ваш номер телефона в нашей базе клиентов.\n\n"
                "Вскоре наш Администратор свяжется с Вами и активирует Ваш доступ к системе.\n\n"
                "Пока наш Администратор активирует Ваш доступ в систему, Вы можете:\n- Узнать больше о нашем центре.\n- Познакомиться с условиями программы лояльности.\n- Посмотреть состав нашей дружной команды.",
                reply_markup=get_user_not_in_db(),
            )
    elif message.text.lower() == "отмена":
        await state.clear()
        await bot.send_message(message.from_user.id, text="Возврат в меню")
    else:
        await message.reply(
            text='Номер должен быть в формате +7XXXXXXXXXX\nПопробуй ещё раз или напиши "Отмена"'
        )


@client_router.callback_query(F.data == "share")
async def send_number(callback: types.CallbackQuery):
    """Предоставление юзеру клавиатуры для отправки номера"""
    await bot.send_message(
        callback.from_user.id,
        text="Нажмите на кнопку, чтобы мы смогли получить ваш номер",
        reply_markup=get_contact(),
    )


@client_router.message(F.content_type.in_({"contact"}))
async def number_received(message: types.Message):
    """Получение из базы данных пользователя по номеру телефона
    Проверка на то, не в чёрном списке ли он и существует ли он вообще в БД
    Происходит получение его телеграм айди для добавления в бд
    """
    user_phone_number = message.contact.phone_number
    user_telegram_id = message.from_user.id
    await bot.send_message(
        message.from_user.id, text="Спасибо! Проверяем вас в базе данных"
    )
    user = ""
    async for client in Client.objects.filter(phone_number=user_phone_number):
        print(client)
        if client:
            user = client
            client.client_telegram_id = user_telegram_id
            await client.asave()
    black_list = []
    if user and user not in black_list:
        await bot.send_message(
            message.from_user.id,
            text=f"*{user.firstName}*, приветствую!\n\nВыберите, что вас интересует ⤵️",
            parse_mode="Markdown",
            reply_markup=get_user_received_from_db(),
        )
    if user and user in black_list:
        await bot.send_message(
            message.from_user.id,
            text="Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна.",
        )
    if not user:
        await bot.send_message(
            message.from_user.id,
            text="К сожалению, я не смог найти Ваш номер телефона в нашей базе клиентов.\n\n"
            "Вскоре наш Администратор свяжется с Вами и активирует Ваш доступ к системе.\n\n"
            "Пока наш Администратор активирует Ваш доступ в систему, Вы можете:\n- Узнать больше о нашем центре.\n- Познакомиться с условиями программы лояльности.\n- Посмотреть состав нашей дружной команды.",
            reply_markup=get_user_not_in_db(),
        )


async def new_appointment(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="Благодарим Вас за обращение!\n\n"
        "В ближайшее время с Вами свяжется Администратор нашей клиники для согласования времени визита.\n\n"
        "Выберите, что Вы хотите сделать? ⤵️",
        reply_markup=get_new_appointment(),
    )


# def register_handlers_client(dp: Dispatcher):
#     dp.register_message_handler(command_start, commands=["start"])
#     dp.register_callback_query_handler(identification, text="1")
#     dp.register_callback_query_handler(send_number, text="share")
#     dp.register_message_handler(number_received, content_types=["contact"])
#     dp.register_callback_query_handler(new_appointment, text="book")
#     dp.register_callback_query_handler(fsm_number, text="write")
#     dp.register_message_handler(fsm_number_get, content_types=["text"], state=FSMPhone)
