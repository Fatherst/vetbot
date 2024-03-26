from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def about_clinic_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Документы для приема 📄", callback_data="appointment_documents"
        ),
        InlineKeyboardButton(text="Схема проезда 🗺️", callback_data="clinic_address"),
        InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
    )
    return markup


def back_to_about_clinic() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Назад 🔙", callback_data="clinic_info"),
    )
    return markup


def clinic_address() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Проложить маршрут 🚘", url=settings.CLINIC_ON_MAP_URL
        ),
        InlineKeyboardButton(text="Назад 🔙", callback_data="clinic_info"),
    )
    return markup
