from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def admin_menu():
    buttons = [
        [
            InlineKeyboardButton(text="Админский интерфейс", callback_data="test"),
        ]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup
