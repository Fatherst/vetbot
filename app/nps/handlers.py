from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings
from bot.bot_init import bot, logger
from telebot import types
from client_auth.models import Client
from appointment.text_generation import get_greeting
from bonuses.models import Program
from bot.states import NpsStates
from nps import keyboards
from client_auth.keyboards import main_menu
from nps import models


def ask_about_review(greeting: str, call: types.CallbackQuery):
    active_program = None
    try:
        active_program = Program.objects.get(is_active=True)
    except Program.DoesNotExist as error:
        logger.error(error)

    text = (
        f"<b>{greeting}</b>,\n\nСпасибо за высокую оценку нашей клиники. Это нас "
        "очень вдохновляет🚀!\n\n"
    )
    if active_program:
        text += (
            "Мы будем благодарны, если Вы поделитесь своими впечатлениями, оставив отзыв "
            "💙\n\nЕсли сделаете скриншот и отправите его нам, с удовольствием начислим Вам "
            f"{active_program.review_bonus_amount} бонусных баллов 🔥"
        )
        reply_markup = keyboards.feedback_buttons()
    else:
        client = Client.objects.get(tg_chat_id=call.message.chat.id)
        reply_markup = main_menu(client)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=text,
        message_id=call.message.message_id,
        reply_markup=reply_markup,
    )


def ask_about_email(greeting: str, call: types.CallbackQuery):
    msg = (
        f"<b>{greeting}</b>,\n\nблагодарим Вас за оценку.\n\nЕсли мы можем стать лучше для "
        "Вас, пожалуйста,поделитесь мнением!"
    )
    reply_markup = keyboards.email_to_manager()
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=msg,
        message_id=call.message.message_id,
        reply_markup=reply_markup,
    )


@bot.callback_query_handler(func=None, config=keyboards.rating_factory.filter())
def process_rating(call: types.CallbackQuery):
    callback_data: dict = keyboards.rating_factory.parse(callback_data=call.data)
    score = int(callback_data["rating"])

    client = Client.objects.get(tg_chat_id=call.message.chat.id)
    greeting = get_greeting(client)

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    models.Rating.objects.create(score=score, client=client, appointment_date=yesterday)

    if score > 8:
        ask_about_review(greeting, call)
    else:
        ask_about_email(greeting, call)


@bot.callback_query_handler(func=lambda c: c.data == "write_email")
def write_email(call: types.CallbackQuery):
    bot.set_state(user_id=call.message.chat.id, state=NpsStates.email)
    client = Client.objects.get(tg_chat_id=call.message.chat.id)
    greeting = get_greeting(client)
    msg = (
        f"<b>{greeting}</b>\n\nблагодарим Вас за оценку.\n\nЕсли мы можем стать лучше для "
        "Вас, пожалуйста, поделитесь мнением!\n\nНапишите ваш отзыв и отправьте его нам"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg
    )


@bot.message_handler(state=NpsStates.email, content_types=["text"])
def send_email(message: types.Message):
    client = Client.objects.get(tg_chat_id=message.chat.id)
    email_msg = (
        f"{message.text}\n\nФИО клиента:{client.full_name}\nНомер телефона:"
        f"{client.phone_number}"
    )
    try:
        send_mail(
            subject="Отзыв от клиента клиники",
            message=email_msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.FEEDBACK_RECIPIENT_EMAIL],
            fail_silently=False,
        )
    except Exception as err:
        logger.error(err, email_msg)
    bot.delete_state(user_id=client.tg_chat_id)
    greeting = get_greeting(client)
    bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>{greeting}</b>,\n\nспасибо за обратную связь, она поможет нам стать лучше!",
        reply_markup=main_menu(client),
    )
