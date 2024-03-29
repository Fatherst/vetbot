from django.conf import settings
from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def back_to_main_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="В главное меню 🔙", callback_data="main_menu"),
    )
    return markup


appointments_factory = CallbackData("appointment_id", prefix="appointment")


def appointments(appointments: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    if appointments:
        for appointment in appointments:
            appointment_date_time = appointment.date_time.strftime(
                "%d.%m.%Y / %H:%M  📆"
            )
            markup.add(
                InlineKeyboardButton(
                    text=appointment_date_time,
                    callback_data=appointments_factory.new(
                        appointment_id=appointment.id,
                    ),
                )
            )
    else:
        markup.add(
            InlineKeyboardButton(
                text="Записаться ✔️", url=settings.CLINIC_MANAGER_TG_URL
            ),
        )
    markup.add(
        InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
    )
    return markup


def manage_appointment(appointment_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Отменить запись ❌", url=settings.CLINIC_MANAGER_TG_URL
        ),
        InlineKeyboardButton(
            text="Перенести запись 📅", url=settings.CLINIC_MANAGER_TG_URL
        ),
        InlineKeyboardButton(
            text="Схема проезда 🗺️",
            callback_data=f"clinic_address.appointment:{appointment_id}",
        ),
        InlineKeyboardButton(text="Назад", callback_data="appointments"),
    )
    return markup


def approve_appointment(appointment_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Подтвердить запись ✔️",
            callback_data=f"approve_appointment:{appointment_id}",
        ),
        InlineKeyboardButton(
            text="Перенести запись 📅", url=settings.CLINIC_MANAGER_TG_URL
        ),
        InlineKeyboardButton(
            text="Отменить запись ❌", url=settings.CLINIC_MANAGER_TG_URL
        ),
    )
    return markup
