from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def bonuses_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Условия программы лояльности 💝", callback_data="loyalty"
        ),
        InlineKeyboardButton(
            text="Получить бонусы за рекомендацию 💲",
            callback_data="recommend_from_bonuses",
        ),
        InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
    )
    return markup


def back_to_bonuses() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Назад 🔙", callback_data="bonuses"),
    )
    return markup


def back_to_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"))
    return markup


def more_bonuses():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="💲 Получить больше бонусов", callback_data="recommend_from_menu"
        )
    )
    return markup
