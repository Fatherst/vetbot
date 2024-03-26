from bot.bot_init import bot
from clinic_info import keyboards
from django.conf import settings
from telebot import apihelper, types


@bot.callback_query_handler(func=lambda c: c.data == "clinic_info")
def clinic_info_callback(call: types.CallbackQuery):
    try:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
    except apihelper.ApiTelegramException:
        pass

    text = (
        "Круглосуточный ветеринарный центр Друзья - в режиме 24/7 мы готовы оказать "
        "профессиональную ветеринарную помощь, без боли, основанную на точной диагностике 🍀\n\n"
        f"Мы всегда на связи: {settings.CLINIC_PHONE}\n"
        f"Наш сайт: {settings.CLINIC_URL}"
    )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.about_clinic_menu(),
        disable_web_page_preview=True,
    )


@bot.callback_query_handler(func=lambda c: c.data == "appointment_documents")
def appointment_documents_callback(call: types.CallbackQuery):
    text = (
        "Пожалуйста, принесите с собой ваш паспорт и ветеринарный паспорт вашего питомца "
        "(при наличии).\nМы работаем круглосуточно 24/7.\n\n"
        f"Мы всегда на связи: {settings.CLINIC_PHONE}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.back_to_about_clinic(),
    )


@bot.callback_query_handler(func=lambda c: c.data == "clinic_address")
def clinic_address_callback(call: types.CallbackQuery):
    try:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
    except apihelper.ApiTelegramException:
        pass

    text = f"<b>Мы находимся по адресу:</b>\n{settings.CLINIC_ADDRESS}"
    path_to_address_image = "clinic_info/imgs/clinic_address.png"
    with open(path_to_address_image, "rb") as address_img:
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=address_img,
            caption=text,
            reply_markup=keyboards.clinic_address(),
        )
