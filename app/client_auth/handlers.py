import random
from sentry_sdk import capture_message
from bot.bot_init import bot, logger
from bot.states import AuthStates
from client_auth import keyboards
from client_auth.models import Client
from django.conf import settings
from integrations.easysms import methods as easysms
from telebot import apihelper, types
from bot.classes import Phone
from appointment.text_generation import get_greeting


def send_old_client_greeting_message(client: Client, message: types.Message):
    if client.enote_id:
        text = (
            f"<b>{get_greeting(client)}</b>, вы успешного авторизованы в нашей бонусной системе! "
            "Но у нас еще много всего интересного для вас 🐾\n\nВыберите, что вас интересует ⤵️"
        )
    else:
        text = (
            "Здравствуйте!\n\nМы не смогли вас найти\n\n😔Выберите, что вас интересует ⤵️\n\n"
            "Прямо сейчас Вы можете:\n- Записаться на прием.\n- Узнать больше о нашем центре.\n- "
            "Познакомиться с условиями программы лояльности.\n- Посмотреть состав нашей дружной "
            "команды."
        )
    bot.send_message(
        chat_id=message.chat.id, text=text, reply_markup=keyboards.main_menu(client)
    )


def send_new_client_greeting_message(message: types.Message):
    text = (
        "Добро пожаловать в ветеринарный центр <b>Друзья</b>! Для начала давайте познакомимся. Для "
        "этого нажмите кнопку <b>Поделиться своим номером.</b>"
    )

    bot.send_message(
        chat_id=message.chat.id, text=text, reply_markup=keyboards.get_contact()
    )


@bot.message_handler(commands=["start"])
def process_start_command(message: types.Message):
    bot.delete_state(user_id=message.chat.id)
    try:
        client = Client.objects.get(tg_chat_id=message.chat.id)
    except Client.DoesNotExist:
        send_new_client_greeting_message(message)
        bot.set_state(user_id=message.chat.id, state=AuthStates.phone)
    else:
        send_old_client_greeting_message(client, message)


def send_sms_message(user_id: int, formatted_phone: str):
    code = random.randrange(1001, 9999)
    code_message = f"Твой код - {code}"
    capture_message(code_message)

    try:
        easysms.send_message(code_message, formatted_phone)
        text = "Напишите код из 4-х цифр, который придет на ваш телефон."
    except Exception as e:
        logger.exception(e)
        text = (
            "Приветствую!\n\nПри попытке отправки кода произошла ошибка, "
            "мы работаем над её устранением, попробуйте позже"
        )
    else:
        bot.set_state(user_id=user_id, state=AuthStates.code)
        bot.add_data(user_id=user_id, code=code, phone=formatted_phone)
    bot.send_message(
        chat_id=user_id, text=text, reply_markup=types.ReplyKeyboardRemove()
    )


def send_non_sms_message(user_id: int, formatted_phone: str):
    code = 1
    text = f"Авторизация по смс отключена, код {code}. Отправьте его"

    bot.set_state(user_id=user_id, state=AuthStates.code)
    bot.add_data(user_id=user_id, code=code, phone=formatted_phone)

    bot.send_message(
        chat_id=user_id, text=text, reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(
    state=AuthStates.phone, phone_is_valid=True, content_types=["text", "contact"]
)
def process_valid_phone(message: types.Message):
    phone = message.text if message.text else message.contact.phone_number
    formatted_phone = Phone.format(phone)

    if settings.USE_EASYSMS:
        send_sms_message(message.chat.id, formatted_phone)
    else:
        send_non_sms_message(message.chat.id, formatted_phone)


@bot.message_handler(
    state=AuthStates.phone, phone_is_valid=False, content_types=["text", "contact"]
)
def process_not_valid_phone(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Отправьте, пожалуйста, российский номер\nПопробуйте ещё раз или напишите /start",
    )


@bot.message_handler(state=AuthStates.code)
def process_code(message: types.Message):
    with bot.retrieve_data(user_id=message.chat.id) as data:
        code = str(data["code"])
        phone = data["phone"]
    if code == message.text:
        defaults = {
            "tg_chat_id": message.chat.id,
            "phone_number": phone,
        }
        client, created = Client.objects.update_or_create(
            phone_number=phone, defaults=defaults
        )
        bot.delete_state(user_id=message.chat.id)
        if client.enote_id:
            text = (
                f"<b>{get_greeting(client)}</b>,вы успешного авторизованы в нашей бонусной системе! "
                "Но у нас еще много всего интересного для вас 🐾\n\nВыберите, что вас интересует ⤵️"
            )
        else:
            text = (
                "Здравствуйте!\n\nМы не смогли вас найти 😔\n\nВыберите, что вас интересует "
                "⤵️\n\n"
                "Прямо сейчас Вы можете:\n- Записаться на прием.\n- Узнать больше о нашем центре.\n- "
                "Познакомиться с условиями программы лояльности.\n- Посмотреть состав нашей дружной "
                "команды."
            )
        reply_markup = keyboards.main_menu(client)
    else:
        text = (
            "Код неправильный, попробуйте ввести ещё раз, либо напишите /start, "
            "чтобы начать сначала"
        )
        reply_markup = None

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda c: c.data == "main_menu")
def process_main_menu_callback(call: types.CallbackQuery):
    try:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
    except apihelper.ApiTelegramException:
        pass
    process_start_command(call.message)
