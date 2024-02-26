from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from bonuses.models import Program


async def get_contact():
    buttons = [[KeyboardButton(text="Поделиться своим номером", request_contact=True)]]
    contact_markup = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Напишите здесь свой номер телефона",
    )
    return contact_markup


async def main_menu(old_client: bool):
    buttons = [
        [
            InlineKeyboardButton(text="Записаться ✔️", callback_data="book"),
        ],
        [
            InlineKeyboardButton(text="О клинике  🏥", callback_data="about"),
        ],
        [
            InlineKeyboardButton(text="Наши врачи 👩‍⚕️", callback_data="doctors"),
        ],
    ]
    if old_client:
        buttons.append(
            [
                InlineKeyboardButton(text="Мои записи 📝", callback_data="appointments"),
            ],
        )
        if await Program.objects.filter(is_active=True).afirst():
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text="Рекомендовать клинику 📢",
                            callback_data="recommend_from_menu",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Мои бонусы 💰", callback_data="bonuses"
                        ),
                    ],
                ]
            )

    else:
        if await Program.objects.filter(is_active=True).afirst():
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Программа лояльности", callback_data="loyalty"
                    ),
                ],
            )
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup
