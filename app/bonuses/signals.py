import asyncio

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from integrations.enote.methods import accrual_post
from bonuses.handlers import message_after_accrual
from bonuses.models import BonusAccural
from asgiref.sync import async_to_sync
from client_auth.management.commands.start_bot import launch_bot

@receiver(post_save, sender=BonusAccural)
def create_bonus_accural(instance, **kwargs):
    print(instance.client.tg_chat_id)
    #accrued = asyncio.run(accrual_post(instance))
    accrued = True
    print(accrued)
    if accrued:
        instance.accured = True
        asyncio.run(message_after_accrual(instance))
        #async_to_sync(message_after_accrual(instance))
        ###send_message_to_user
    ##else log
    ###Поставить в очередь в celery на следующий день
