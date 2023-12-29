from aiogram import types
from .keyboards import (
    get_contact,
    main_menu_kb,
)
from .models import Client
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import Command, Filter
import re
import random
import logging
from api_methods.methods import easy_send_code


logger = logging.getLogger(__name__)
client_router = Router()


class PhoneFilter(Filter):
    mask = r"([78][0-9]{10})"

    async def __call__(self, message: types.Message) -> bool:
        row_phone_number = message.text
        phone_number = re.sub(r"\D", "", row_phone_number)
        phone_mask = re.compile(self.mask)
        return re.fullmatch(phone_mask, phone_number)


class PhoneStates(StatesGroup):
    phone = State()
    code = State()


async def authenticate_user(
    user_id: int,
) -> tuple[str, str, types.InlineKeyboardMarkup]:
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    if client:
        if client.first_name:
            greeting = f"{client.first_name}, приветствую"
        else:
            greeting = "Приветствую"
        return (
            greeting,
            "<b>Выберите, что вас интересует ⤵</b>",
            await main_menu_kb(bool(client.enote_id)),
        )
    else:
        return (
            "<b>Добро пожаловать в бота ветеринарного центра Друзья 🐈</b>\n\n"
            "Для начала мне нужно вас идентифицировать в качестве клиента нашей клиники. "
            "Для этого, пожалуйста, нажмите на кнопку чтобы отправить свой номер телефона, "
            "указанный в Telegram, или напишите его вручную",
            "",
            await get_contact(),
        )


@client_router.message(Command("start"))
async def send_greeting(message: types.Message, state: FSMContext):
    await state.clear()
    greeting, text, reply_markup = await authenticate_user(message.from_user.id)
    await message.answer(
        text=f"{greeting}\n\n{text}",
        reply_markup=reply_markup,
    )
    if not text:  # Проверка на наличие текста для установки состояния FSM
        await state.set_state(PhoneStates.phone)


async def process_client_phone(
    state: FSMContext, user_phone_number: str, message: types.Message
):
    """Проверку на то, есть ли пользователь я вообще убрал, теперь только проверка на черный список"""
    black_list = []
    user_phone_number = re.sub(r"\D", "", user_phone_number)
    client = await Client.objects.filter(
        phone_number__contains=user_phone_number[1:]
    ).afirst()
    if client in black_list:
        await message.answer(
            text="Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна.",
        )
        await state.clear()
    else:
        # code = random.randrange(1001, 9999)
        code = 1
        await state.update_data(code=code)
        code_sent = await easy_send_code(code, user_phone_number)
        print(code_sent)
        if code_sent == True:
            await state.update_data(phone_number=user_phone_number)
            await message.answer(
                text="Приветствую!\n\n"
                "Напишите код из 4-х цифр, который придёт на ваш телефон",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            await state.set_state(PhoneStates.code)
        else:
            await message.answer(
                text="Приветствую!\n\n"
                "Не получилось прислать код на указанный номер телефона, попробуйте прислать телефон ещё раз",
                reply_markup=await get_contact(),
            )


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
    await process_client_phone(
        state=state,
        user_phone_number=message.contact.phone_number,
        message=message,
    )


@client_router.message(PhoneStates.code, F.text)
async def handle_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if str(data["code"]) == message.text:
        defaults = {
            "tg_chat_id": message.from_user.id,
            "phone_number": data["phone_number"],
        }
        client, created = await Client.objects.aupdate_or_create(
            phone_number__contains=data["phone_number"][1:], defaults=defaults
        )
        await state.clear()
        await message.answer(
            text="Вы успешно авторизовались в клиентской части бота",
            reply_markup=await main_menu(bool(client.enote_id)),
        )
    else:
        await message.answer(
            text="Код неправильный, попробуй ввести ещё раз, либо напиши /start, чтобы начать сначала",
        )


@client_router.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    greeting, text, reply_markup = await authenticate_user(callback.from_user.id)
    await callback.message.edit_text(
        text=f"{greeting}\n\n{text}",
        reply_markup=reply_markup,
    )
