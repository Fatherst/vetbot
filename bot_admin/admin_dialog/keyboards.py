from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)





def get_admin_code():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton("Получить код", callback_data="email")
    inline_markup.add(b1)
    return inline_markup


def admin_menu():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton("Админский интерфейс", callback_data="test")
    inline_markup.add(b1)
    return inline_markup