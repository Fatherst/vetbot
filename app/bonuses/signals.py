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
    loop = asyncio.get_event_loop()
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    accrued = loop.run_until_complete(accrual_post(instance))
    print(accrued)
    if accrued:
        instance.accured = True
        #asyncio.set_event_loop(loop)
        loop.run_until_complete(message_after_accrual(instance))
        #asyncio.ensure_future(message_after_accrual(instance))
        # asyncio.run(message_after_accrual(instance))
        #async_to_sync(message_after_accrual(instance))
        ###send_message_to_user
    ##else log
    ###Поставить в очередь в celery на следующий день
