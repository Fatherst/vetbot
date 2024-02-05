import asyncio
from asgiref.sync import sync_to_async
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from integrations.enote.methods import accrual_enote
from bonuses.models import BonusAccrual
from bot_admin.create_bot import bot
import requests
from django.conf import settings


@receiver(pre_save, sender=BonusAccrual)
def create_bonus_accural(instance, **kwargs):
    if instance.accrued:
        accrued = accrual_enote(instance)
        if accrued:
            old_instance = BonusAccrual.objects.filter(id=instance.id).first()
            BonusAccrual.objects.filter(id=instance.id).update(accrued=True)
            if instance.accrued != old_instance.accrued:
                requests.get(
                    f"https://api.telegram.org/bot{settings.BOT_API_TOKEN}/sendMessage",
                    params={
                        "chat_id": instance.client.tg_chat_id,
                        "text": f"Вам начислено {instance.amount} бонусов",
                    },
                )
