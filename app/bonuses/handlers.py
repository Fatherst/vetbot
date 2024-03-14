import random
import string

from bonuses import keyboards
from bonuses.models import Program, Recommendation
from bot.bot_init import bot
from client_auth.models import Client
from telebot import types


def create_program_description(program: Program) -> str:
    text = (
        "В рамках программы лояльности Клиника начисляет Клиентам бонусные "
        "баллы (кешбэк), которые можно использовать для оплаты услуг Клиники.\n\n"
        f"{program.description}\n\nРазмер кешбэка зависит от статуса "
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
        f"\n\nКроме этого, Клиника подарит {program.new_client_bonus_amount} бонусных "
        "баллов за каждого нового Клиента, которому Вы рекомендовали нашу Клинику."
    )
    return program_description + status_description + new_client_description


@bot.callback_query_handler(func=lambda c: c.data == "bonuses")
def bonus_program(call: types.CallbackQuery):
    program = Program.objects.filter(is_active=True).first()
    client = Client.objects.get(tg_chat_id=call.from_user.id)

    balance_info = client.balance
    name = client.full_name if client.full_name else "Уважаемый клиент"
    balance_message = (
        f"Баланс Вашего бонусного счета: {balance_info.bonus_balance} "
        "бонусных баллов.\n\n"
    )
    status_message = ""

    status = program.retrieve_status(balance_info.money_spent)
    if status:
        status_message = (
            f"на данный момент Ваш статус в программе лояльности:\n\n<b>{status.name}</b>"
            f"\n\nЭто значит, что Вы получаете {status.cashback_amount}% бонусными "
            "баллами с потраченной в Клинике суммы!\n\n"
        )
    text = f"<b>{name}</b>, {status_message}{balance_message}{program.description}"
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

    name = client.full_name if client.full_name else "Уважаемый клиент"
    text = (
        f"<b>{name}</b>, мы безмерно ценим, когда нас рекомендуют!\n\nПоэтому мы начислим "
        f"{program.new_client_bonus_amount} бонусных баллов на Ваш счет в Клинике "
        f"и {program.new_client_bonus_amount} приветственных баллов Вашему другу "
        "или родственнику в знак благодарности за каждого нашего будущего Клиента, "
        "которому Вы порекомендуете наш Центр. \n\nЧтобы рекомендовать нас,перешлите "
        "промокод клиенту, который собирается прийти в клинику ⤵️\n\nВаш промокод: "
        f"{promocode}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=reply_markup,
    )
