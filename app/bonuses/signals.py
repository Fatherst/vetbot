from django.dispatch import receiver
from django.db.models.signals import post_save
from bonuses.models import BonusAccrual, Recommendation, Program
from bonuses.tasks import accrual_bonuses_by_enote
from bot.bot_init import bot, logger
from bonuses import keyboards
from appointment.text_generation import get_greeting


@receiver(post_save, sender=BonusAccrual)
def accrue_bonuses(created, instance, **kwargs):
    if created and not instance.client.in_blacklist:
        accrual_bonuses_by_enote.delay(instance.id)


@receiver(post_save, sender=BonusAccrual)
def send_notification(instance, **kwargs):
    if instance.accrued and instance.tracker.has_changed("accrued"):
        client = instance.client
        greeting = get_greeting(client)
        program = Program.objects.filter(is_active=True).first()
        REASONS = {
            "REGISTRATION": "Бонус за подключение к боту ветеринарного центра <b>Друзья</b> 🐈!",
            "BIRTHDAY": "С любовью, ваши Друзья!",
            "REFERAL_GETTER": "Бонус за принятие приглашения в клинику!",
            "REFERAL_SENDER": "Бонус за приглашенного в клинику клиента!",
            "REVIEW": "Бонус за отзыв!",
            "MANUAL": "Вам были вручную начислены бонусы!",
        }
        DEFAULT_REASON = "Вам были начислены бонусы!"
        reason_message = REASONS.get(instance.reason, DEFAULT_REASON)
        if instance.reason == "BIRTHDAY":
            text = (
                f"<b>{greeting}</b>, поздравляем вашего друга с днем рождения и желаем еще многих "
                "счастливых  и здоровых лет. Пусть он всегда будет полон энергии, "
                f"любви и шалостей.\n\nВ честь праздника мы дарим вам <b>{instance.amount} "
                "бонусных баллов</b>, которые  вы можете использовать для оплаты услуг в нашем "
                f"центре.\n\n<b>{program.description}</b>\n\n{reason_message}"
            )
        else:
            text = (
                f"<b>{greeting}</b>, Вам начислено <b>{instance.amount} бонусных баллов</b>\n\nВы можете "
                f"использовать их для оплаты услуг в нашем Центре\n\n<b>{program.description}</b>\n"
                f"\n{reason_message}"
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
