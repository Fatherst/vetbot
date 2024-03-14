import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from bonuses.models import BonusAccrual, Recommendation, Program
from bonuses.tasks import accrual_bonuses_by_enote
from bot.bot_init import bot, logger
from bonuses import keyboards


@receiver(post_save, sender=BonusAccrual)
def accrue_bonuses(created, instance, **kwargs):
    if created:
        accrual_bonuses_by_enote.delay(instance.id)


@receiver(post_save, sender=BonusAccrual)
def send_notification(instance, **kwargs):
    if instance.accrued and instance.tracker.has_changed("accrued"):
        client = instance.client
        name = client.full_name if client.full_name else "Уважаемый клиент"

        REASONS = {
            "REGISTRATION": "Бонус за подключение к боту ветеринарного центра Друзья 🐈!",
            "BIRTHDAY": "Бонус на день рождения пациента!",
            "REFERAL_GETTER": "Бонус за принятие приглашения в клинику!",
            "REFERAL_SETTER": "Бонус за приглашенного в клинику клиента!",
            "MANUAL": "Вам были вручную начислены бонусы!",
        }
        DEFAULT_REASON = "Вам были начислены бонусы!"
        reason_message = REASONS.get(instance.reason, DEFAULT_REASON)

        text = (
            f"<b>{name}</b>, Вам начислено {instance.amount} бонусных баллов\n\nВы можете "
            f"использовать их для оплаты услуг в нашем Центре\n\n1 бонусный балл = 1 "
            f"рубль\n\n{reason_message}"
        )
        bot.send_message(
            chat_id=client.tg_chat_id, text=text, reply_markup=keyboards.more_bonuses()
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
        else:
            BonusAccrual.objects.create(
                client=instance.client,
                amount=active_program.new_client_bonus_amount,
                reason="REFERAL_SENDER",
            )
