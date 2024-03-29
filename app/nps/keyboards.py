from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telebot.callback_data import CallbackData


rating_factory = CallbackData("rating", prefix="rating")


def get_rating() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = [
        InlineKeyboardButton(
            text=rating,
            callback_data=rating_factory.new(rating=rating),
        )
        for rating in range(1, 11)
    ]
    markup.add(*buttons)
    return markup


def email_to_manager() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Написать руководству", callback_data="write_email"),
    )
    return markup


def feedback_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Оставить отзыв на Yandex Я", callback_data="link_yandex"
        ),
        InlineKeyboardButton(
            text="Оставить отзыв на Google G", callback_data="link_google"
        ),
    )
    return markup
