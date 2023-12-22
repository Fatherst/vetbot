from aiogram import types
from .keyboards import (
    get_contact,
    user_main_menu,
    not_enote_main_menu,
    back,
    back_or_loyalty,
    back_or_loyalty_or_recomend,
)
from .models import Client
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import Command, Filter
import re
import random
import aiohttp
from django.conf import settings
from aiohttp.client_exceptions import ClientResponseError
import logging


logger = logging.getLogger(__name__)
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


async def get_user_data(user_id: int) -> tuple[str, str, types.InlineKeyboardMarkup]:
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    if client:
        if client.first_name:
            greeting = f"{client.first_name}, приветствую"
        else:
            greeting = "Приветствую"
        if client.enote_id:
            return greeting, "<b>Выберите, что вас интересует ⤵</b>", user_main_menu()
        else:
            return (
                greeting,
                "<b>Выберите, что вас интересует ⤵</b>",
                not_enote_main_menu(),
            )
    else:
        return (
            "<b>Добро пожаловать в бота ветеринарного центра Друзья 🐈</b>\n\n"
            "Для начала мне нужно вас идентифицировать в качестве клиента нашей клиники. "
            "Для этого, пожалуйста, нажмите на кнопку чтобы отправить свой номер телефона, "
            "указанный в Telegram, или напишите его вручную",
            "",
            get_contact(),
        )


@client_router.message(Command("start"))
async def send_greeting(message: types.Message, state: FSMContext):
    """
    Проверка на то, зарегистрирован ли пользователь уже
    """
    await state.clear()
    greeting, text, reply_markup = await get_user_data(message.from_user.id)
    await message.answer(
        text=f"{greeting}\n\n{text}",
        reply_markup=reply_markup,
    )
    if text == "":  # Проверка на наличие текста для установки состояния FSM
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
        client = await Client.objects.filter(phone_number=data["phone_number"]).afirst()
        await state.clear()
        if client.enote_id:
            reply_markup = user_main_menu()
        else:
            reply_markup = not_enote_main_menu()
        await message.answer(
            text="Вы успешно авторизовались в клиентской части бота",
            reply_markup=reply_markup,
        )
    else:
        await message.answer(
            text="Код неправильный, попробуй ввести ещё раз, либо напиши /start, чтобы начать сначала",
        )


@client_router.callback_query(F.data == "back")
async def main_menu(callback: types.CallbackQuery):
    greeting, _, reply_markup = await get_user_data(callback.from_user.id)
    await callback.message.edit_text(
        text=f"{greeting}\n\nВыберите, что вас интересует ⤵",
        reply_markup=reply_markup,
    )


@client_router.callback_query(F.data == "bonuses")
async def bonuses_program(callback: types.CallbackQuery):
    client = await Client.objects.filter(tg_chat_id=callback.from_user.id).afirst()
    query_params = {
        "client_enote_id": client.enote_id,
        "department_enote_id": "9c0d9196-5a62-4508-ad92-e3ade9b247d8",
    }
    headers = {"apikey": settings.APIKEY, "Authorization": settings.BASIC_AUTH}
    balance = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://ru.enote.link/79c0973a-3b89-11ec-f988-12896acfa599-e5/hs/api/v1/balance",
                params=query_params,
                headers=headers,
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                balance = body["totalBalanceClient"]
    except ClientResponseError as error:
        logger.error(error)
    if balance:
        msg = (
            f"на данный момент Ваш статус в программе лояльности:\n\n<b>БРОНЗОВЫЙ</b>\n\nЭто значит, что Вы получаете"
            f" 3% бонусными баллами с потраченной в Клинике суммы!\n\nБаланс Вашего бонусного счета: {balance} бонусных баллов.\n\nВы можете оплатить бонусами до 20% от стоимости услуг Клиники!\n\n1 бонусный балл = 1 рубль"
        )
        reply_markup = back_or_loyalty_or_recomend()
    else:
        msg = "к сожалению, у вас пока нет бонусного счёта, вы сможете открыть его при посещении клиники"
        reply_markup = back_or_loyalty()
    await callback.message.edit_text(
        text=f"<b>{callback.from_user.first_name}</b>, {msg}",
        reply_markup=reply_markup,
    )


@client_router.callback_query(F.data == "loyalty")
async def loyalty_program(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="В рамках программы лояльности Клиника начисляет Клиентам бонусные баллы (кешбэк), которые можно использовать для оплаты услуг Клиники.\n\n 1 бонусный балл = 1 рубль\n\nРазмер кешбэка зависит от статуса Клиента в программе лояльности:\n\nБронзовый статус - кешбэк 3%\n\nКлиент оплатил услуг Клиники на 0 - 9999 руб\n\nСеребряный статус - кешбэк 5%\n\nКлиент оплатил услуг Клиники на 10000 - 29999 руб\n\nЗолотой статус - кешбэк 8%\n\nКлиент оплатил услуг Клиники на 30000 - 49999 руб\n\nПлатиновый статус - кешбэк 10%\n\nКлиент оплатил услуг Клиники на сумму более 50000 руб\n\nВы можете оплатить бонусами до 10% стоимости услуг хирургии и до 20% от стоимости услуг терапии Клиники!\n\nКроме этого, Клиника подарит 1000 бонусных баллов за каждого нового Клиента, которому Вы рекомендовали нашу Клинику.",
        reply_markup=back(),
    )
