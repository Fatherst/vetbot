from bonuses.models import BonusAccrual, Program
from client_auth.models import Client
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Client)
def accrue_bonuses_after_registration(instance, **kwargs):
    if instance.tracker.has_changed("tg_chat_id") and not instance.tracker.previous(
        "tg_chat_id"
    ):
        try:
            active_program = Program.objects.get(is_active=True)
        except Program.DoesNotExist:
            return
        registration_bonus_exists = BonusAccrual.objects.filter(
            client=instance, reason="REGISTRATION"
        ).exists()
        if not registration_bonus_exists:
            BonusAccrual.objects.create(
                client=instance,
                amount=active_program.registration_bonus_amount,
                reason="REGISTRATION",
            )
