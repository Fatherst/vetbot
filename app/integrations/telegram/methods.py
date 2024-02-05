import requests
from django.conf import settings
from bonuses.models import BonusAccrual


def send_message_after_accrual(instance: BonusAccrual):
    requests.get(
        f"https://api.telegram.org/bot{settings.BOT_API_TOKEN}/sendMessage",
        params={
            "chat_id": instance.client.tg_chat_id,
            "text": f"Вам начислено следующее количество бонусов: {instance.amount}",
        },
    )
