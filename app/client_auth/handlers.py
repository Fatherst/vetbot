import re
import random
import logging
from typing import NamedTuple
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import Command, Filter
from django.conf import settings
from integrations.easysms.methods import easy_send_code
from client_auth import keyboards
from .models import Client

logger = logging.getLogger(__name__)
client_router = Router()


class PhoneFilter(Filter):
    mask = r"([78][0-9]{10})"

    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            row_phone_number = message.text
        else:
            row_phone_number = message.contact.phone_number
        phone_number = re.sub(r"\D", "", row_phone_number)
        phone_mask = re.compile(self.mask)
        return re.fullmatch(phone_mask, phone_number)


class PhoneStates(StatesGroup):
    phone = State()
    code = State()


class AuthResult(NamedTuple):
    greeting: str
    new_client: bool
    reply_markup: types.InlineKeyboardMarkup


async def prepare_authentication_response(
    user_id: int,
) -> AuthResult:
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    if client:
        if client.first_name and client.middle_name and client.last_name:
            greeting = (f"<b>{client.last_name} {client.first_name} {client.middle_name}</b>, "
                        f"приветствую\n\n<b>Выберите, "
                        f"что вас интересует "
                        f"⤵</b>")
        else:
            greeting = "Приветствую\n\n<b>Выберите, что вас интересует ⤵</b>"
        return AuthResult(
            greeting,
            False,
            await keyboards.main_menu(bool(client.enote_id)),
        )
    else:
        return AuthResult(
            "<b>Добро пожаловать в бота ветеринарного центра Друзья 🐈</b>\n\n"
            "Для начала мне нужно вас идентифицировать в качестве клиента нашей клиники. "
            "Для этого, пожалуйста, нажмите на кнопку чтобы отправить свой номер телефона, "
            "указанный в Telegram, или напишите его вручную",
            True,
            await keyboards.get_contact(),
        )


@client_router.message(Command("start"))
async def send_greeting(message: types.Message, state: FSMContext):
    await state.clear()
    result = await prepare_authentication_response(message.from_user.id)
    await message.answer(
        text=result.greeting,
        reply_markup=result.reply_markup,
    )
    if result.new_client:  # Проверка на наличие текста для установки состояния FSM
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
        logger.info(f"USE_EASY_SMS = {settings.USE_EASY_SMS}")
        if settings.USE_EASY_SMS:
            code = random.randrange(1001, 9999)
            code_sent = await easy_send_code(code, "7" + user_phone_number[1:])
            text = "Приветствую!\n\n" \
                   "Напишите код из 4-х цифр, который придёт на ваш телефон"
        else:
            code = 1
            code_sent = True
            text = f"Авторизация по смс отключена, код {code}. Отправьте его"
        logger.info(f"code = {code}")
        if code_sent:
            await state.update_data(code=code)
            await state.update_data(phone_number=user_phone_number)
            await message.answer(
                text=text,
                reply_markup=types.ReplyKeyboardRemove(),
            )
            await state.set_state(PhoneStates.code)
        else:
            await message.answer(
                text="Приветствую!\n\n"
                "При попытке отправки кода произошла ошибка, мы работаем над её устранением, "
                "попробуйте позже",
                reply_markup=await keyboards.get_contact(),
            )


@client_router.message(PhoneStates.phone, F.text, PhoneFilter())
async def handle_correct_text_contact(message: types.Message, state: FSMContext):
    phone_number = re.sub(r"\D", "", message.text)
    await process_client_phone(
        state=state,
        user_phone_number=phone_number,
        message=message,
    )


@client_router.message(
    PhoneStates.phone, PhoneFilter(), F.content_type.in_({"contact"})
)
async def handle_contact(message: types.Message, state: FSMContext):
    await process_client_phone(
        state=state,
        user_phone_number=message.contact.phone_number,
        message=message,
    )


@client_router.message(PhoneStates.phone, F.text, lambda x: x != PhoneFilter())
async def handle_wrong_text_contact(message: types.Message):
    await message.reply(
        text="Пришли,пожалуйста, российский номер\nПопробуй ещё раз или напиши /start"
    )


@client_router.message(
    PhoneStates.phone, lambda x: x != PhoneFilter(), F.content_type.in_({"contact"})
)
async def handle_wrong_contact(message: types.Message):
    await message.reply(
        text="Пришли,пожалуйста, российский номер\nПопробуй ещё раз или напиши /start"
    )


@client_router.message(PhoneStates.code, F.text)
async def handle_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    logger.info(f"user data = {str(data)}")
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
            reply_markup=await keyboards.main_menu(bool(client.enote_id)),
        )
    else:
        await message.answer(
            text="Код неправильный, попробуй ввести ещё раз, либо напиши /start, чтобы начать сначала",
        )


@client_router.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    result = await prepare_authentication_response(callback.from_user.id)
    await callback.message.edit_text(
        text=result.greeting,
        reply_markup=result.reply_markup,
    )
