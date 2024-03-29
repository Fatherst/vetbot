import random
import string

from bonuses import keyboards
from bonuses.models import Program, Recommendation
from bot.bot_init import bot
from client_auth.models import Client
from telebot import types
from appointment.text_generation import get_greeting


def create_program_description(program: Program) -> str:
    text = (
        "В рамках программы лояльности Клиника начисляет Клиентам бонусные "
        "баллы (кешбэк), которые можно использовать для оплаты услуг Клиники.\n\n"
        f"<b>{program.description}</b>\n\nРазмер кешбэка зависит от статуса "
        "Клиента в программе лояльности:"
    )
    return text


def generate_statuses_description(program: Program) -> str:
    program_description = create_program_description(program)

    status_description = ""
    for status in program.statuses.order_by("start_amount"):
        if status.end_amount:
            status_description += (
                f"\n\n<b>{status.name} статус</b> - кешбэк {status.cashback_amount}%\n<i>Клиент "
                f"оплатил услуг Клиники на {status.start_amount} - {status.end_amount} руб</i>"
            )
        else:
            status_description += (
                f"\n\n<b>{status.name} статус</b> - кешбэк {status.cashback_amount}%\n<i>Клиент "
                f"оплатил услуг Клиники на {status.start_amount} и больше руб</i>"
            )

    new_client_description = (
        f"\n\nВы можете оплатить бонусами до <b>{program.payment_percent}%</b> стоимости любой "
        "услуги.\n\nКроме этого, "
        f"мы подарим вам <b>{program.new_client_bonus_amount}</b> бонусных "
        "баллов за каждого нового друга, которому Вы порекомендуете нашу Клинику.\n\n💙"
    )
    return program_description + status_description + new_client_description


@bot.callback_query_handler(func=lambda c: c.data == "bonuses")
def bonus_program(call: types.CallbackQuery):
    program = Program.objects.filter(is_active=True).first()
    client = Client.objects.get(tg_chat_id=call.from_user.id)

    balance_info = client.balance
    balance_message = (
        f"Баланс Вашего бонусного счета:<b> {balance_info.bonus_balance} "
        "бонусных баллов.</b>\n\n"
    )
    status_message = ""
    payment_message = (
        f"Вы можете оплатить до <b>{program.payment_percent}%</b> от стоимости "
        "услуг Клиники!\n\n"
    )
    status = program.retrieve_status(balance_info.money_spent)
    if status:
        status_message = (
            f"на данный момент Ваш статус в программе лояльности:\n\n<b>{status.name}</b>"
            f"\n\nЭто значит, что Вы получаете <b>{status.cashback_amount}%</b> бонусными "
            "баллами с потраченной в Клинике суммы!\n\n"
        )
    text = (
        f"<b>{get_greeting(client)}</b>, {status_message}{balance_message}{payment_message}"
        f"<b>{program.description}</b>"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboards.bonuses_menu(),
    )


@bot.callback_query_handler(func=lambda c: c.data == "loyalty")
def program_status(call: types.CallbackQuery):
    client = Client.objects.get(tg_chat_id=call.from_user.id)
    program = Program.objects.filter(is_active=True).first()

    if client.enote_id:
        reply_markup = keyboards.back_to_bonuses()
    else:
        reply_markup = keyboards.back_to_main_menu()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=generate_statuses_description(program),
        reply_markup=reply_markup,
    )


def create_promocode() -> str:
    while True:
        SIZE = 6
        promocode = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=SIZE)
        )
        is_unique = not Recommendation.objects.filter(promocode=promocode).exists()
        if is_unique:
            return promocode


@bot.callback_query_handler(
    func=lambda c: c.data in ["recommend_from_bonuses", "recommend_from_menu"]
)
def get_promocode(call: types.CallbackQuery):
    client = Client.objects.get(tg_chat_id=call.from_user.id)
    program = Program.objects.filter(is_active=True).first()

    promocode = create_promocode()
    Recommendation.objects.create(promocode=promocode, client=client)

    if call.data == "recommend_from_menu":
        reply_markup = keyboards.back_to_main_menu()
    else:
        reply_markup = keyboards.back_to_bonuses()

    text = (
        f"<b>{get_greeting(client)}</b>, благодарим Вас за доверие 💙\n\nМы начислим Вам "
        f"<b>{program.new_client_bonus_amount}</b> бонусных баллов за рекомендацию 🔥\n\n"
        f"И начислим {program.new_client_bonus_amount} приветственных баллов Вашему другу 🍀\n\n"
        f"Для этого поделитесь с ним данным промокодом: {promocode}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=reply_markup,
    )
