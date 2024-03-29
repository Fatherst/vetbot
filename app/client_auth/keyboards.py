from bonuses.models import Program
from client_auth.models import Client
from django.conf import settings
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

    if active_program_exists and client_with_enote_id:
        markup.add(
            InlineKeyboardButton(text="Мои бонусы 💰", callback_data="bonuses"),
            InlineKeyboardButton(
                text="Рекомендовать клинику 📢",
                callback_data="recommend_from_menu",
            ),
        )

    if client_with_enote_id:
        markup.add(
            InlineKeyboardButton(text="Мои записи 📝", callback_data="appointments"),
        )

    elif active_program_exists:
        markup.add(
            InlineKeyboardButton(text="Программа лояльности 🐱", callback_data="loyalty")
        )
    markup.add(
        InlineKeyboardButton(text="Записаться ✔️", url=settings.CLINIC_MANAGER_TG_URL),
        InlineKeyboardButton(text="О клинике  🏥", callback_data="clinic_info"),
        InlineKeyboardButton(text="Наши врачи 👩‍⚕️", callback_data="doctors"),
    )
    return markup
