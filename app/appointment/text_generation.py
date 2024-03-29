from datetime import datetime

from appointment import models
from client_auth.models import Client
from django.conf import settings


def get_greeting(client: Client) -> str:
    if client.first_name:
        return f"{client.first_name}"
    return "Уважаемый клиент"


def get_msg_header(greeting: str, appointment_date: str, is_notification: bool) -> str:
    if is_notification:
        return (
            f"<b>{greeting}</b>, напоминаю Вам, что завтра <b>{appointment_date}</b> Вы "
            "записаны в нашу Клинику:\n\n"
        )
    return (
        f"<b>{greeting}</b>, Вы записаны на приём:\n\n<b>Дата:</b> {appointment_date}\n"
    )


MONTHS = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def format_date(date: datetime) -> str:
    return f"{date.day:02d} {MONTHS[date.month]} {date.year}"


def get_appointment_description(
    appointment: models.Appointment, is_notification: bool
) -> str:
    doctor_name = (
        appointment.doctor.full_name if appointment.doctor else "Врач не назначен"
    )
    greeting = get_greeting(appointment.client)
    appointment_date = format_date(appointment.date_time)
    appointment_time = appointment.date_time.strftime("%H:%M")
    msg_header = get_msg_header(greeting, appointment_date, is_notification)
    text = (
        f"{msg_header}<b>Время:</b> {appointment_time}\n<b>"
        f"Ваш врач:</b> {doctor_name}\n"
        f"<b>Адрес:</b> {settings.CLINIC_ADDRESS}\n\n"
        "Пожалуйста, с собой принесите ваш паспорт и ветеринарный паспорт вашего питомца (при "
        "наличии).\n\nДля отмены или переноса записи нажмите одну из кнопок ниже ⤵️"
    )
    return text
