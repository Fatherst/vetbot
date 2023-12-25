from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


async def get_contact():
    buttons = [[KeyboardButton(text="Поделиться своим номером", request_contact=True)]]
    contact_markup = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Напишите здесь свой номер телефона",
    )
    return contact_markup


async def main_menu_kb(old_client: bool):
    if old_client:
        buttons = [
            [
                InlineKeyboardButton(text="Мои бонусы 💰", callback_data="bonuses"),
            ],
            [
                InlineKeyboardButton(text="Мои записи 📝", callback_data="appointments"),
            ],
            [
                InlineKeyboardButton(text="Записаться ✔️", callback_data="book"),
            ],
            [
                InlineKeyboardButton(
                    text="Рекомендовать клинику 📢", callback_data="recommend"
                ),
            ],
            [
                InlineKeyboardButton(text="О клинике  🛈", callback_data="about"),
            ],
            [
                InlineKeyboardButton(text="Наши врачи 👩‍⚕️", callback_data="doctors"),
            ],
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(text="Записаться ✔️", callback_data="book"),
            ],
            [
                InlineKeyboardButton(
                    text="Программа лояльности", callback_data="loyalty"
                ),
            ],
            [
                InlineKeyboardButton(text="О клинике  🏥", callback_data="about"),
            ],
            [
                InlineKeyboardButton(text="Наши врачи 👩‍⚕️", callback_data="doctors"),
            ],
        ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup


def get_new_appointment():
    buttons = [
        [
            InlineKeyboardButton(text="Мои бонусы 💰", callback_data="bonuses"),
            InlineKeyboardButton(text="Мои записи 📝", callback_data="appointments"),
            InlineKeyboardButton(
                text="Рекомендовать клинику 📢", callback_data="recommend"
            ),
            InlineKeyboardButton(text="О клинике  🛈", callback_data="about"),
            InlineKeyboardButton(text="Наши врачи 👩‍⚕️", callback_data="doctors"),
            InlineKeyboardButton(text="Назад 🔙", callback_data="menu"),
        ]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_markup
