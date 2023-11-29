from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)





def get_admin_code():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton("Получить код", callback_data="admin_email")
    inline_markup.add(b1)
    return inline_markup
