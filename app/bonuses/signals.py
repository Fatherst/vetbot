import asyncio

from django.dispatch import receiver
from django.db.models.signals import post_save
from integrations.enote.methods import accrual_post
from bonuses.handlers import message_after_accrual
from bonuses.models import BonusAccural


@receiver(post_save, sender=BonusAccural)
def create_bonus_accural(instance, **kwargs):
    async def async_accrual(instance):
        accrued = await accrual_post(instance)
        print(accrued)
        accrued = True
        if accrued:
            instance.accured = True
            await message_after_accrual(instance)
        ##else
        ###Поставить в очередь в celery на следующий день

    asyncio.run(async_accrual(instance))
