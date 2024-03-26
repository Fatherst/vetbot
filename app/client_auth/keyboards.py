from bonuses.models import Program
from client_auth.models import Client
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def get_contact() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Напишите здесь свой номер телефона",
    )
    markup.add(KeyboardButton(text="Поделиться своим номером", request_contact=True))
    return markup


def main_menu(client: Client) -> InlineKeyboardMarkup:
    active_program_exists = Program.objects.filter(is_active=True).exists()
    client_with_enote_id = client.enote_id

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="О клинике  🏥", callback_data="clinic_info"),
        InlineKeyboardButton(text="Наши врачи 👩‍⚕️", callback_data="doctors"),
    )

    if client_with_enote_id:
        markup.add(
            InlineKeyboardButton(text="Мои записи 📝", callback_data="appointments"),
        )

    if active_program_exists and client_with_enote_id:
        markup.add(
            InlineKeyboardButton(
                text="Рекомендовать клинику 📢",
                callback_data="recommend_from_menu",
            ),
            InlineKeyboardButton(text="Мои бонусы 💰", callback_data="bonuses"),
        )

    elif active_program_exists:
        markup.add(
            InlineKeyboardButton(text="Программа лояльности 💰", callback_data="loyalty")
        )
    return markup
