from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from integrations.enote.methods import add_bonus_points
from bonuses.models import BonusAccrual
from integrations.telegram.methods import send_message_after_accrual


@receiver(pre_save, sender=BonusAccrual)
def update_bonus_accrual(instance, **kwargs):
    if instance.accrued:
        enote_accrued = add_bonus_points(instance)
        if enote_accrued:
            instance.accrued = True
        else:
            instance.accrued = False
            ### ставить в очередь


@receiver(post_save, sender=BonusAccrual)
def send_notification(instance, **kwargs):
    if instance.accrued and instance.tracker.has_changed("accrued"):
        send_message_after_accrual(instance)
