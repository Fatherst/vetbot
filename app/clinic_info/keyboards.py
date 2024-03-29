from appointment.models import Doctor, Specialization
from django.conf import settings
from django.db.models.query import QuerySet
from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def about_clinic_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Документы для приема 📄", callback_data="appointment_documents"
        ),
        InlineKeyboardButton(
            text="Схема проезда 🗺️", callback_data="clinic_address.clinic_info"
        ),
        InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
    )
    return markup


def back_to_about_clinic() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Записаться ✔️", url=settings.CLINIC_MANAGER_TG_URL),
        InlineKeyboardButton(text="Назад 🔙", callback_data="clinic_info"),
    )
    return markup


def clinic_address(back_callback_data: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Проложить маршрут 🚘", url=settings.CLINIC_ON_MAP_URL
        ),
        InlineKeyboardButton(text="Назад 🔙", callback_data=back_callback_data),
    )
    return markup


specializations_factory = CallbackData("specialization_id", prefix="specialization")


def specializations_menu(
    specializations: QuerySet[Specialization],
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for specialization in specializations:
        markup.add(
            InlineKeyboardButton(
                text=specialization.name,
                callback_data=specializations_factory.new(
                    specialization_id=specialization.id,
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(text="Назад 🔙", callback_data="main_menu"),
    )
    return markup


doctors_factory = CallbackData("doctor_id", prefix="doctor")


def doctors_menu(doctors: QuerySet[Doctor]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for doctor in doctors:
        markup.add(
            InlineKeyboardButton(
                text=doctor.full_name,
                callback_data=doctors_factory.new(
                    doctor_id=doctor.id,
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(text="Назад 🔙", callback_data="doctors"),
    )
    return markup


def doctor_menu(
    doctors: QuerySet[Doctor], specialization_id: int
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for doctor in doctors:
        markup.add(
            InlineKeyboardButton(
                text=doctor.full_name,
                callback_data=doctors_factory.new(
                    doctor_id=doctor.id,
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(
            text="Назад 🔙",
            callback_data=specializations_factory.new(
                specialization_id=specialization_id,
            ),
        ),
    )
    return markup
