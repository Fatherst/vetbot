from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData


def back_to_main_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="В главное меню 🔙", callback_data="main_menu"),
    )
    return markup


appointments_factory = CallbackData("appointment_id", prefix="appointment")


def appointments(appointments: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for appointment in appointments:
        appointment_date = appointment.date_time.strftime("%d.%m.%Y")
        appointment_time = appointment.date_time.strftime("%H:%M")
        markup.add(
            InlineKeyboardButton(
                text=f"{appointment_date} / {appointment_time}  📆",
                callback_data=appointments_factory.new(
                    category_id=appointment.id,
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
    )
    return markup


def manage_appointment(appointment_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Отменить запись ❌", callback_data="cancel_appointment"
        ),
        InlineKeyboardButton(
            text="Перенести запись 📅", callback_data="change_appointment"
        ),
        InlineKeyboardButton(text="Назад", callback_data="appointments"),
    )
    return markup
