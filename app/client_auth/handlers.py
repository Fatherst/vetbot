from aiogram import types
from .keyboards import (
    get_contact,
    get_user_main_menu,
)
from .models import Client
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import Command, Filter
import re
import random


client_router = Router()


class PhoneFilter(Filter):
    mask = r"(7[0-9]{10})"

    async def __call__(self, message: types.Message) -> bool:
        row_phone_number = message.text
        phone_number = re.sub(r"\D", "", row_phone_number)
        phone_mask = re.compile(self.mask)
        return re.fullmatch(phone_mask, phone_number)


class PhoneStates(StatesGroup):
    phone = State()
    code = State()


@client_router.message(Command("start"))
async def send_greeting(message: types.Message, state: FSMContext):
    """
    Проверка на то, зарегистрирован ли пользователь уже
    """
    await state.clear()
    user_id = message.from_user.id
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    if client:
        if client.first_name:
            greeting = f"{client.first_name}, приветствую"
        else:
            greeting = "Приветствую"
        await message.answer(
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
        await message.answer(
            text=greeting,
            reply_markup=get_contact(),
        )
        await state.set_state(PhoneStates.phone)


async def process_client_phone(
    state: FSMContext, user_phone_number: str, message: types.Message
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


@client_router.message(PhoneStates.phone, F.text, PhoneFilter())
async def handle_correct_text_contact(message: types.Message, state: FSMContext):
    phone_number = re.sub(r"\D", "", message.text)
    await process_client_phone(
        state=state,
        user_phone_number=phone_number,
        message=message,
    )


@client_router.message(PhoneStates.phone, F.text, lambda x: x != PhoneFilter())
async def handle_wrong_text_contact(message: types.Message):
    await message.reply(
        text="Пришли,пожалуйста, российский номер\nПопробуй ещё раз или напиши /start"
    )


@client_router.message(PhoneStates.phone, F.content_type.in_({"contact"}))
async def handle_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    phone_number = re.sub(r"\D", "", phone_number)
    await process_client_phone(
        state=state,
        user_phone_number=phone_number,
        message=message,
    )


@client_router.message(PhoneStates.code, F.text)
async def handle_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if str(data["code"]) == message.text:
        await Client.objects.aupdate_or_create(
            phone_number=data["phone_number"], tg_chat_id=message.from_user.id
        )
        await state.clear()
        await message.answer(
            text="Вы успешно авторизовались в клиентской части бота",
            reply_markup=get_user_main_menu(),
        )
    else:
        await message.answer(
            text="Код неправильный, попробуй ввести ещё раз, либо напиши /start, чтобы начать сначала",
        )
