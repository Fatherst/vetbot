from django.dispatch import receiver
import logging
from django.db.models.signals import post_save
from bonuses.models import BonusAccrual, Recommendation, Program
from integrations.telegram.methods import send_message
from .tasks import accrual_bonuses_by_enote

logger = logging.getLogger(__name__)


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


@receiver(post_save, sender=Recommendation)
def accrue_recommendation_bonus(instance, **kwargs):
    if instance.issued and instance.tracker.has_changed("issued"):
        try:
            active_program = Program.objects.get(is_active=True)
        except Program.DoesNotExist as error:
            instance.issued = False
            instance.save()
            logger.error(error)
            return
        BonusAccrual.objects.create(
            client=instance.client,
            amount=active_program.new_client_bonus_amount,
            reason="REFERAL_SENDER",
        )
