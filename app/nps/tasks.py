from datetime import datetime, timedelta
from django.db.models import Max
from bot_admin.celery import app
from bot.bot_init import bot, logger
from client_auth.models import Client
from nps import keyboards
from appointment.text_generation import get_greeting


@app.task
def send_nps():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    clients_with_appointments = (
        Client.objects.filter(
            appointments__status="COMPLETED",
            appointments__date_time__date=yesterday,
            appointments__patient__time_of_death=None,
        )
        .exclude(tg_chat_id=None)
        .exclude(deleted=True)
        .exclude(appointments__deleted=True)
        .exclude(in_blacklist__isnull=False)
        .annotate(latest_appointment=Max("appointments__date_time"))
    )
    for client in clients_with_appointments:
        msg = (
            f"<b>{get_greeting(client)}, здравствуйте!</b>\n\nНам очень важно знать как"
            " прошло ваше последнее посещение нашего ветеринарного центра Друзья "
            "⭐️\n\nПожалуйста,  оцените его от 1 до 10, где:\n\n1 - <b>Очень плохо</b>\n10 - "
            "<b>Очень хорошо</b>"
        )
        try:
            bot.send_message(
                chat_id=client.tg_chat_id,
                text=msg,
                reply_markup=keyboards.get_rating(),
            )
        except Exception:
            pass
