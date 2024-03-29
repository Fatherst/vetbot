from telebot.apihelper import ApiTelegramException
from bonuses.models import BonusAccrual, Program
from nps.models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver
from bot.bot_init import bot
from appointment.text_generation import get_greeting
from nps.keyboards import feedback_buttons


def generate_rejection_message(rejection_reason):
    if rejection_reason == "WRONG_CLINIC":
        text = (
            "для начисления бонусов просим поделиться  "
            "мнением о нашем ветеринарном центре Друзья ⭐️"
        )
    else:
        text = "для начисления бонусов за отзыв просим прислать корректный скриншот 📲"
    return text


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
            f"<b>{active_program.review_bonus_amount}</b> бонусных баллов скоро будут начислены "
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
            f"<b>{get_greeting(instance.client)}</b>, "
            f"{generate_rejection_message(instance.rejection_reason)}\n\nПожалуйста, прикрепите  "
            f"скриншот отзыва, и мы начислим вам <b>{active_program.review_bonus_amount}</b> "
            "бонусных баллов 💰"
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
