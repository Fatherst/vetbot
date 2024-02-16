from django.dispatch import receiver
import logging
from django.db.models.signals import post_save
from .models import Client
from bonuses.models import BonusAccrual, Program

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Client)
def accrue_bonuses_after_registration(instance, **kwargs):
    if instance.tracker.has_changed("tg_chat_id") and not instance.tracker.previous(
        "tg_chat_id"
    ):
        try:
            active_program = Program.objects.get(is_active=True)
        except Program.DoesNotExist as error:
            logger.error(error)
            return
        registration_bonus = BonusAccrual.objects.filter(
            client=instance, reason="REGISTRATION"
        ).first()
        if not registration_bonus:
            BonusAccrual.objects.create(
                client=instance,
                amount=active_program.registration_bonus_amount,
                reason="REGISTRATION",
            )
