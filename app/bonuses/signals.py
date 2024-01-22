from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


from bonuses.models import BonusAccural


@receiver(post_save, sender=BonusAccural)
def create_bonus_accural(instance, created, **kwargs):
    print(instance)
    print("dsdzx")
    ###Начислить бонусы
    ###if начислено
    instance.accured = True
    ###send_message_to_client
    ###send_message_to_user
    ##else log
    ###Поставить в очередь в celery на следующий день
