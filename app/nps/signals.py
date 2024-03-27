from telebot.apihelper import ApiTelegramException
from bonuses.models import BonusAccrual, Program
from nps.models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver
from bot.bot_init import bot
from appointment.text_generation import get_greeting
from nps.keyboards import feedback_buttons


@receiver(post_save, sender=Review)
def process_status_change(instance, **kwargs):
    if not instance.tracker.has_changed("status"):
        return
    try:
        active_program = Program.objects.get(is_active=True)
    except Program.DoesNotExist:
        return
    if instance.status == "APPROVED":
        text = (
            f"<b>{get_greeting(instance.client)}</b>, отзыв успешно проверен, "
            f"{active_program.review_bonus_amount} бонусных баллов скоро будут начислены "
            f"на ваш лицевой счет  💰\n\nДо новых встреч в ветеринарном центре Друзья 😻"
        )
        BonusAccrual.objects.create(
            client=instance.client,
            amount=active_program.review_bonus_amount,
            reason="REVIEW",
        )
        reply_markup = None

    elif instance.status == "REJECTED":
        text = (
            f"<b>{get_greeting(instance.client)}</b>, для начисления бонусов за отзыв просим прислать "
            "корректный скриншот 📲\n\nПожалуйста, прикрепите скриншот отзыва, и мы начислим "
            f"вам {active_program.review_bonus_amount} бонусных баллов 💰"
        )
        reply_markup = feedback_buttons()
    else:
        return
    try:
        bot.send_message(
            chat_id=instance.client.tg_chat_id,
            text=text,
            reply_markup=reply_markup,
        )
    except ApiTelegramException:
        pass
