from appointment.models import Doctor, Specialization
from bot.bot_init import bot, logger
from bot.states import ClinicInfoStates
from client_auth.models import Client
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
        "(при наличии).\nМы работаем круглосуточно 24/7 🕑\n\n"
        f"Мы всегда на связи: {settings.CLINIC_PHONE}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.back_to_about_clinic(),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("clinic_address"))
def clinic_address_callback(call: types.CallbackQuery):
    back_callback_data = call.data.split(".")[-1]
    try:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
    except apihelper.ApiTelegramException:
        pass

    text = f"<b>Мы находимся по адресу:</b>\n{settings.CLINIC_ADDRESS}"
    path_to_address_image = "clinic_info/imgs/clinic_address.jpg"
    with open(path_to_address_image, "rb") as address_img:
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=address_img,
            caption=text,
            reply_markup=keyboards.clinic_address(back_callback_data),
        )


@bot.callback_query_handler(func=lambda c: c.data == "doctors")
def doctors_callback(call: types.CallbackQuery):
    specializations = Specialization.objects.filter(show_in_bot=True)
    text = "Выберите направление, которое Вас интересует ⤵️"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.specializations_menu(specializations),
    )


@bot.callback_query_handler(
    func=None, config=keyboards.specializations_factory.filter()
)
def specializations_callback(call: types.CallbackQuery):
    try:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
    except apihelper.ApiTelegramException:
        pass

    callback_data: dict = keyboards.specializations_factory.parse(
        callback_data=call.data
    )
    specialization_id = int(callback_data["specialization_id"])

    specialization = Specialization.objects.get(id=specialization_id)
    doctors = specialization.doctors.filter(show_in_bot=True, fired_date=None).exclude(
        deleted=True
    )

    bot.set_state(user_id=call.message.chat.id, state=ClinicInfoStates.doctors)
    bot.add_data(
        user_id=call.message.chat.id, chosen_specialization_id=specialization_id
    )

    text = f"Специалисты направления <b>{specialization.name}</b>  ⤵️"
    bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.doctors_menu(doctors),
    )


def generate_doctor_description(doctor: Doctor, client: Client) -> str:
    if client.first_name:
        greeting = f"{client.first_name}, знакомьтесь!"
    else:
        greeting = "Знакомьтесь!"

    positions = doctor.positions.filter(show_in_bot=True)
    positions_description = (
        ", ".join([position.name for position in positions])
        if positions
        else "сотрудник ветеринарной клиники"
    )

    text = (
        f"{greeting}\n\n"
        f"{doctor.full_name}, {positions_description}\n\n"
        f"{doctor.detail_info}"
    )

    return text


@bot.callback_query_handler(func=None, config=keyboards.doctors_factory.filter())
def doctor_callback(call: types.CallbackQuery):
    try:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
    except apihelper.ApiTelegramException:
        pass

    callback_data: dict = keyboards.doctors_factory.parse(callback_data=call.data)
    doctor_id = int(callback_data["doctor_id"])

    with bot.retrieve_data(user_id=call.message.chat.id) as data:
        chosen_specialization_id = data["chosen_specialization_id"]

    doctor = Doctor.objects.get(id=doctor_id)
    client = Client.objects.get(tg_chat_id=call.message.chat.id)
    text = generate_doctor_description(doctor, client)

    specialization = Specialization.objects.get(id=chosen_specialization_id)
    other_doctors = (
        specialization.doctors.filter(show_in_bot=True, fired_date=None)
        .exclude(deleted=True)
        .exclude(id=doctor_id)
    )
    reply_markup = keyboards.doctor_menu(other_doctors, chosen_specialization_id)

    if doctor.photo:
        try:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=doctor.photo,
                caption=text,
                reply_markup=reply_markup,
            )
            return
        except Exception as e:
            logger.exception(e)

    bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=reply_markup,
    )
