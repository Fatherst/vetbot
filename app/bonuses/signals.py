import asyncio
import json
from django.dispatch import receiver
import logging
from django.db.models.signals import post_save
from bonuses.models import BonusAccrual, Recommendation, Program
from integrations.telegram.methods import send_message
from .tasks import accrual_bonuses_by_enote
from bonuses.handlers import retrieve_greeting

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BonusAccrual)
def accrue_bonuses(created, instance, **kwargs):
    if created:
        accrual_bonuses_by_enote.delay(instance.id)


@receiver(post_save, sender=BonusAccrual)
def send_notification(instance, **kwargs):
    if instance.accrued and instance.tracker.has_changed("accrued"):
        full_name = instance.client.full_name
        greeting = asyncio.run(retrieve_greeting(full_name))
        reason_messages = {
            "REGISTRATION": "Бонус за подключение к боту ветеринарного центра Друзья 🐈!",
            "BIRTHDAY": "Бонус на день рождения пациента!",
            "REFERAL_GETTER": "Бонус за принятие приглашения в клинику!",
            "REFERAL_SETTER": "Бонус за приглашенного в клинику клиента!",
            "MANUAL": "Вам были вручную начислены бонусы!",
        }
        reason_message = reason_messages.get(
            instance.reason, "Вам были начислены бонусы!"
        )
        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "💲 Получить больше бонусов",
                        "callback_data": "recommend_from_menu",
                    }
                ]
            ]
        }
        msg = (
            f"{greeting}Вам начислено {instance.amount} бонусных баллов\n\nВы можете "
            f"использовать их для оплаты услуг в нашем Центре\n\n1 бонусный балл = 1 "
            f"рубль\n\n{reason_message}"
        )
        send_message(
            instance.client.tg_chat_id,
            text=msg,
            reply_markup=json.dumps(reply_markup),
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
