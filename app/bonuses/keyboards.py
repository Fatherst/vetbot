from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def bonuses_menu():
    buttons = [
        [
            InlineKeyboardButton(
                text="Условия программы лояльности 💝", callback_data="loyalty"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Получить бонусы за рекомендацию 💲",
                callback_data="recommend_from_bonuses",
            ),
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
        ],
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup


async def back_to_bonuses():
    buttons = [
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="bonuses"),
        ],
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup


async def back_to_menu():
    buttons = [
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
        ],
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup
