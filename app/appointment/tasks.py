from datetime import datetime, timedelta
from appointment.models import Appointment
from bot_admin.celery import app
from bot.bot_init import bot, logger
from appointment import keyboards
from appointment.text_generation import get_appointment_description


@app.task
def send_appointment_notification():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    appointments = (
        Appointment.objects.filter(
            date_time__date=tomorrow,
            status="PLANNED",
        )
        .exclude(
            deleted=True,
        )
        .exclude(client__tg_chat_id=None)
    )
    for appointment in appointments:
        msg = get_appointment_description(appointment, True)
        try:
            bot.send_message(
                chat_id=appointment.client.tg_chat_id,
                text=msg,
                reply_markup=keyboards.approve_appointment(appointment.id),
            )
        except Exception as err:
            logger.exception(err)
