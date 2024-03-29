from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Админский интерфейс", callback_data="test"),
    )
    return markup
