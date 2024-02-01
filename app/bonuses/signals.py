import asyncio

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from integrations.enote.methods import accrual_enote
from bonuses.models import BonusAccrual
from bot_admin.create_bot import bot


@receiver(post_save, sender=BonusAccrual)
def create_bonus_accural(instance, **kwargs):
    async def async_accrual(instance):
        accrued = await accrual_enote(instance)
        print(accrued)
        accrued = True
        if accrued:
            instance.accured = True
            #await instance.asave()
            await bot.send_message(
                instance.client.tg_chat_id,
                f"Вам начислено {instance.amount} бонусов",
            )
        ##else
        ###Поставить в очередь в celery на следующий день

    asyncio.run(async_accrual(instance))

# @receiver(post_save, sender=BonusAccrual)
# def send_message_after_accrual(instance, **kwargs):
#     async def async_send_message_after_accrual(instance):
#         if instance.pk:
#             old_value = BonusAccrual.objects.get(pk=instance.pk).accured
#             if instance.accured != old_value:
#                 await bot.send_message(
#                     instance.client.tg_chat_id,
#                     f"Вам начислено {instance.amount} бонусов",
#                 )
#     asyncio.run(async_send_message_after_accrual(instance))
