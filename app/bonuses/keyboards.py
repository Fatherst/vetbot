from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def bonuses_menu(has_balance: bool):
    buttons = [
        [
            InlineKeyboardButton(
                text="Условия программы лояльности 💝", callback_data="loyalty"
            ),
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
        ],
    ]

    if has_balance:
        buttons.insert(
            1,
            [
                InlineKeyboardButton(
                    text="Получить 1000 бонусов за рекомендацию 💲",
                    callback_data="recommend",
                ),
            ],
        )
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup


async def back_to_bonuses_or_menu(has_enote_id: bool):
    callback_data = "main_menu"
    if has_enote_id:
        callback_data = "bonuses"
    buttons = [
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=callback_data),
        ],
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup
