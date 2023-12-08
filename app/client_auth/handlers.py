from aiogram import types
from .keyboards import (
    get_contact,
    get_user_main_menu,
)
from aiogram import Bot
from .models import Client
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import Command, and_f, Filter
import re
import random


client_router = Router()


class PhoneFilter(Filter):
    def __init__(self, mask: str) -> None:
        self.mask = mask

    async def __call__(self, message: types.Message) -> bool:
        row_phone_number = message.text
        phone_number = re.sub(r"\D", "", row_phone_number)
        phone_mask = re.compile(self.mask)
        return re.fullmatch(phone_mask, phone_number)


class PhoneStates(StatesGroup):
    phone = State()
    code = State()


@client_router.message(Command("start"))
async def user_greet(message: types.Message, bot: Bot, state: FSMContext):
    """
    Проверка на то, зарегистрирован ли пользователь уже
    """
    await state.clear()
    user_id = message.from_user.id
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    if client:
        if client.first_name is not None:
            greeting = f"{client.first_name}, приветствую"
        else:
            greeting = "Приветствую"
        await bot.send_message(
            message.from_user.id,
            text=f"<b>{greeting}</b>\n\nВыберите, что вас интересует ⤵",
            reply_markup=get_user_main_menu(),
        )
    else:
        greeting = (
            "Добро пожаловать в бота ветеринарного центра <b>Друзья</b> 🐈\n"
            "Для начала мне нужно Вас идентифицировать в качестве клиента нашей клиники. "
            "Для этого, пожалуйста,нажмите на кнопку чтобы отправить свой номер телефона,"
            " указанный в Telegram, или напишите его вручную"
        )
        await bot.send_message(
            message.from_user.id,
            text=greeting,
            reply_markup=get_contact(),
        )
        await state.set_state(PhoneStates.phone)


async def client_state_update(
    state: FSMContext, user_phone_number, message: types.Message
):
    """Проверку на то, есть ли пользователь я вообще убрал, теперь только проверка на черный список"""
    black_list = []
    client = await Client.objects.filter(phone_number=user_phone_number).afirst()
    if client not in black_list:
        # code = random.randrange(1001, 9999)
        code = 1
        await state.update_data(code=code)
        await state.update_data(phone_number=user_phone_number)
        await message.answer(
            text="Приветствую!\n\n"
            "Напишите код из 4-х цифр, который придёт на ваш телефон",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.set_state(PhoneStates.code)
    else:
        await message.answer(
            text="Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна.",
        )
        await state.clear()


@client_router.message(PhoneStates.phone, F.text, PhoneFilter(mask=r"(7[0-9]{10})"))
async def recieve_text_number_true(message: types.Message, state: FSMContext):
    phone_number = re.sub(r"\D", "", message.text)
    await client_state_update(
        state=state,
        user_phone_number=phone_number,
        message=message,
    )


@client_router.message(
    PhoneStates.phone, F.text, lambda x: x != PhoneFilter(mask=r"(7[0-9]{10})")
)
async def recieve_text_number_false(message: types.Message):
    await message.reply(
        text="Пришли,пожалуйста, российский номер\nПопробуй ещё раз или напиши /start"
    )


@client_router.message(PhoneStates.phone, F.content_type.in_({"contact"}))
async def recieve_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    phone_number = re.sub(r"\D", "", phone_number)
    await client_state_update(
        state=state,
        user_phone_number=phone_number,
        message=message,
    )


@client_router.message(PhoneStates.code, F.text)
async def recieve_code_confirmation(
    message: types.Message, state: FSMContext, bot: Bot
):
    data = await state.get_data()
    if str(data["code"]) == message.text:
        await Client.objects.aupdate_or_create(
            phone_number=data["phone_number"], tg_chat_id=message.from_user.id
        )
        await state.clear()
        await bot.send_message(
            message.from_user.id,
            text="Вы успешно авторизовались в клиентской части бота",
            reply_markup=get_user_main_menu(),
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="Код неправильный, попробуй ввести ещё раз, либо напиши /start, чтобы начать сначала",
        )
