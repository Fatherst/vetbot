import random
from admin_auth import keyboards
from admin_auth.models import Admin
from bot.bot_init import bot
from bot.states import AdminAuthStates
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from telebot import types


@bot.message_handler(commands=["admin"])
def admin_command(message: types.Message):
    bot.delete_state(user_id=message.chat.id)
    admin = Admin.objects.filter(tg_chat_id=message.from_user.id).first()
    if admin:
        bot.send_message(
            chat_id=message.chat.id,
            text="Ты попал в админ-панель!",
            reply_markup=keyboards.main_menu(),
        )
    else:
        text = (
            "Пожалуйста, введи свою электронную почту, на которую"
            " тебя зарегистрировали в качестве администратора"
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
        )
        bot.set_state(user_id=message.chat.id, state=AdminAuthStates.email)


@bot.message_handler(state=AdminAuthStates.email)
def handle_admin_email(message: types.Message):
    email = message.text
    user = User.objects.filter(email=email).first()
    if user:
        code = random.randrange(1001, 9999)
        text = (
            "Вы найдены в базе данных администраторов\nНа вашу почту отправлен код,"
            " напишите его здесь"
        )
        bot.set_state(user_id=message.chat.id, state=AdminAuthStates.code)
        bot.add_data(user_id=message.chat.id, admin_id=user.id, code=code)
        send_mail(
            subject="Код",
            message=f"Ваш код {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f"{email}"],
            fail_silently=False,
        )
    else:
        text = "Вы не найдены в базе администраторов"

    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(state=AdminAuthStates.code)
def handle_admin_email_code(message: types.Message):
    with bot.retrieve_data(user_id=message.chat.id) as data:
        user_id = data["admin_id"]
        code = str(data["code"])
    if code == message.text:
        Admin.objects.create(user_id=user_id, tg_chat_id=message.from_user.id)
        bot.delete_state(message.chat.id)
        text = "Вы успешно авторизовались в админской части бота"
        reply_markup = keyboards.main_menu()
    else:
        text = "Код неправильный, попробуйте ещё раз или нажмите /admin, чтобы начать сначала"
        reply_markup = None
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup)
