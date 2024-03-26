from appointment import keyboards, models
from bot.bot_init import bot
from client_auth.models import Client
from django.utils import timezone
from telebot import types
from appointment.text_generation import get_appointment_description


@bot.callback_query_handler(func=None, config=keyboards.appointments_factory.filter())
def manage_appointment(call: types.CallbackQuery):
    callback_data: dict = keyboards.appointments_factory.parse(callback_data=call.data)
    appointment_id = int(callback_data["appointment_id"])

    appointment = models.Appointment.objects.get(id=appointment_id)
    msg = get_appointment_description(appointment, False)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=msg,
        reply_markup=keyboards.manage_appointment(),
    )


@bot.callback_query_handler(func=lambda c: c.data == "appointments")
def appointments_menu(call: types.CallbackQuery):
    client = Client.objects.get(tg_chat_id=call.from_user.id)
    today = timezone.now()
    appointments = client.appointments.filter(date_time__gte=today)
    if appointments:
        text = (
            "На данный момент у Вас есть запланированные приемы в нашей клинике "
            "на следующие даты.\n\nВыберите дату для просмотра деталей записи ⤵️"
        )
    else:
        text = "На данный момент у вас нет запланированных приёмов в клинике"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.appointments(appointments),
    )


@bot.callback_query_handler(func=lambda c: c.data == "about_clinic")
def about_clinic_callback(call: types.CallbackQuery):
    text = (
        "Круглосуточный ветеринарный центр Друзья - в режиме 24/7 мы готовы оказать "
        "профессиональную ветеринарную помощь, без боли, основанную на точной диагностике 🍀\n\n"
        "Мы всегда на связи: +7 (4922) 49-47-82\n"
        "Наш сайт: https://vetfriends.ru"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.about_clinic_menu(),
        disable_web_page_preview=True,
    )
