import asyncio
from asgiref.sync import sync_to_async
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from integrations.enote.methods import accrual_enote
from bonuses.models import BonusAccrual
from bot_admin.create_bot import bot


# @receiver(post_save, sender=BonusAccrual)
# def create_bonus_accural(instance, **kwargs):
#     async def async_accrual(instance):
#         accrued = accrual_enote(instance)
#         print(accrued)
#         accrued = True
#         if accrued:
#             instance.accured = True
#             print('pre')
#             BonusAccrual.objects.filter(id=instance.id).aupdate(accrued=True)
#             await bot.send_message(
#                 instance.client.tg_chat_id,
#                 f"Вам начислено {instance.amount} бонусов",
#             )
#         ##else
#         ###Поставить в очередь в celery на следующий день
#
#     # loop = asyncio.new_event_loop()
#     # asyncio.set_event_loop(loop)
#     # asyncio.get_event_loop().run_until_complete(async_accrual(instance))
#
#     #asyncio.run(async_accrual(instance))
#
#     asyncio.new_event_loop().run_until_complete(async_accrual(instance))

# @receiver(pre_save, sender=BonusAccrual)
# def send_message_after_accrual(instance, **kwargs):
#     async def async_send_message_after_accrual(instance):
#         if instance.pk:
#             print(instance.accured)
#             print('sd')
#             ### Проверка на то, поменялось ли поле accured
#             old_value = await BonusAccrual.objects.filter(id=instance.id).afirst()
#             print('after')
#             if instance.accured != old_value.accured and instance.accured == True:
#                 print('zx')
#                 await bot.send_message(
#                     instance.client.tg_chat_id,
#                     f"Вам начислено {instance.amount} бонусов",
#                 )
#     print('here')
#     asyncio.run(async_send_message_after_accrual(instance))

@receiver(post_save, sender=BonusAccrual)
def create_bonus_accural(instance, **kwargs):
    # accrued = asyncio.run(accrual_enote(instance))
    accrued = accrual_enote(instance)
    print(accrued)
    accrued = True
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if accrued:
        print('pre')
        BonusAccrual.objects.filter(id=instance.id).update(accrued=True)
        try:
            loop = asyncio.get_event_loop()
            send = asyncio.run_coroutine_threadsafe(bot.send_message(
                instance.client.tg_chat_id,
                f"Вам начислено {instance.amount} бонусов",
            ), loop=loop)
            send.result()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            send = asyncio.run_coroutine_threadsafe(bot.send_message(
                instance.client.tg_chat_id,
                f"Вам начислено {instance.amount} бонусов",
            ), loop=loop)
            send.result()
    ##else
    ###Поставить в очередь в celery на следующий день

# @receiver(pre_save, sender=BonusAccrual)
# def send_message_after_accrual(instance, **kwargs):
#     if instance.pk:
#         print(instance.accrued)
#         print('sd')
#         ### Проверка на то, поменялось ли поле accured
#         old_value = BonusAccrual.objects.filter(id=instance.id).first()
#         print('after')
#         if instance.accrued != old_value.accrued and instance.accrued == True:
#             print('zx')
#             # await bot.send_message(
#             #     instance.client.tg_chat_id,
#             #     f"Вам начислено {instance.amount} бонусов",
#             # )
#     print('here')