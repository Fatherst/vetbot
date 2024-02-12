from django.dispatch import receiver
from django.db.models.signals import post_save
from bonuses.models import BonusAccrual
from integrations.telegram.methods import send_message
from .tasks import accrual_bonuses_by_enote


@receiver(post_save, sender=BonusAccrual)
def accrue_bonuses(created, instance, **kwargs):
    if created:
        accrual_bonuses_by_enote.delay(instance.id)


@receiver(post_save, sender=BonusAccrual)
def send_notification(instance, **kwargs):
    if instance.accrued and instance.tracker.has_changed("accrued"):
        send_message(
            instance.client.tg_chat_id,
            text=f"Вам начислено следующее количество бонусов: {instance.amount}",
        )
