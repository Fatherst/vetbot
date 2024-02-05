from django.dispatch import receiver
from django.db.models.signals import pre_save
from integrations.enote.methods import accrual_enote
from bonuses.models import BonusAccrual
import requests
from django.conf import settings


@receiver(pre_save, sender=BonusAccrual)
def update_bonus_accrual(instance, **kwargs):
    if instance.accrued:
        accrued = accrual_enote(instance)
        if accrued:
            BonusAccrual.objects.filter(id=instance.id).update(accrued=True)


@receiver(pre_save, sender=BonusAccrual)
def send_notification(instance, **kwargs):
    if instance.accrued and instance.accrued != (instance.tracker.previous("accrued")):
        requests.get(
            f"https://api.telegram.org/bot{settings.BOT_API_TOKEN}/sendMessage",
            params={
                "chat_id": instance.client.tg_chat_id,
                "text": f"Вам начислено {instance.amount} бонусов",
            },
        )
