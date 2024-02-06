from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from integrations.enote.methods import add_bonus_points
from bonuses.models import BonusAccrual
from integrations.telegram.methods import send_message


@receiver(post_save, sender=BonusAccrual)
def accrue_bonuses(created, instance, **kwargs):
    if created:
        enote_accrued = add_bonus_points(instance)
        if enote_accrued:
            instance.accrued = True
            instance.save()


@receiver(post_save, sender=BonusAccrual)
def send_notification(created, instance, **kwargs):
    if created and instance.accrued:
        send_message(
            instance.client.tg_chat_id,
            text=f"Вам начислено следующее количество бонусов: {instance.amount}",
        )
