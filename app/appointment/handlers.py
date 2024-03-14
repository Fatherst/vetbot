from appointment import keyboards, models
from bot.bot_init import bot
from client_auth.models import Client
from django.utils import timezone
from telebot import types


@bot.callback_query_handler(func=lambda c: c.data == "book")
def create_appointment(call: types.CallbackQuery):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Ссылка на чат",
        reply_markup=keyboards.back_to_main_menu()
    )


@bot.callback_query_handler(func=lambda c: c.data == "cancel_appointment")
def cancel_appointment(call: types.CallbackQuery):
    text = "ОТМЕНЕН\n\n В ближайшее время с Вами свяжется Администратор нашей клиники для " \
           "согласования более  удобного для Вас времени визита."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.back_to_main_menu(),
    )


@bot.callback_query_handler(func=lambda c: c.data == "change_appointment")
def change_appointment(call: types.CallbackQuery):
    text = "ПРИНЯТО \n\nВ ближайшее время с Вами свяжется Администратор нашей клиники для " \
           "согласования более удобного для Вас времени визита."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.back_to_main_menu(),
    )


@bot.callback_query_handler(
    func=None, appointments_config=keyboards.appointments_factory.filter()
)
def manage_appointment(call: types.CallbackQuery):
    callback_data: dict = keyboards.appointments_factory.parse(callback_data=call.data)
    appointment_id = int(callback_data['appointment_id'])

    appointment = models.Appointment.objects.get(id=appointment_id)
    doctor = appointment.doctor
    appointment_date = appointment.date_time.strftime("%d.%m.%Y в %H:%M")
    appointment_time = appointment.date_time.strftime("%H:%M")
    text = (
        "Вы записаны на прием:\n\n"
        f"<b>Дата:</b> {appointment_date}\n<b>Время:</b> {appointment_time}\n<b>"
        f"Ваш врач: </b>{doctor.first_name} {doctor.last_name}\n"
        "<b>Адрес:</b> Владимир, ул. Студеная Гора, 44А/2\n\n"
        "С собой необходимо принести ваш паспорт и ветеринарный "
        "паспорт животного (при наличии).\n\n"
        "Для отмены или переноса записи нажмите одну из кнопок ниже ⤵️\n\n"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.manage_appointment(appointment_id),
    )


@bot.callback_query_handler(func=lambda c: c.data == "appointments")
def appointments_menu(call: types.CallbackQuery):
    client = Client.objects.get(tg_chat_id=call.from_user.id)
    today = timezone.now()
    appointments = client.appointments.filter(date_time__gte=today)
    if appointments:
        text = "На данный момент у Вас есть запланированные приемы в нашей клинике " \
               "на следующие даты.\n\nВыберите дату для просмотра деталей записи ⤵️"
    else:
        text = "На данный момент у вас нет запланированных приёмов в клинике"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.appointments(appointments),
    )
