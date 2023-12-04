from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)





def get_admin_code():
    buttons = [
        [
        InlineKeyboardButton(text="Получить код", callback_data="email"),
        ]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup


def admin_menu():
    buttons = [
        [
        InlineKeyboardButton(text="Админский интерфейс", callback_data="test"),
        ]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup