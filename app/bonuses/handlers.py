import logging
import string
import random
from aiogram import Router, F
from aiogram import types
from asgiref.sync import sync_to_async
from sentry_sdk import capture_message
from .keyboards import bonuses_menu, back_to_menu, back_to_bonuses
from client_auth.keyboards import main_menu
from client_auth.models import Client
from bonuses.models import Program, Recommendation

logger = logging.getLogger(__name__)


bonuses_router = Router()


async def retrieve_greeting(full_name):
    if full_name:
        greeting = f"<b>{full_name}</b>, "
    else:
        greeting = "<b>Уважаемый клиент</b>, "
    return greeting


async def create_description(program: Program):
    text = (
        "В рамках программы лояльности Клиника начисляет Клиентам бонусные баллы (кешбэк), "
        f"которые можно использовать для оплаты услуг Клиники.\n\n{program.description}\n\nРазмер кешбэка зависит от статуса"
        " Клиента в программе лояльности:"
    )
    return text


@bonuses_router.callback_query(F.data == "bonuses")
async def bonuses_program(callback: types.CallbackQuery):
    program = await Program.objects.filter(is_active=True).afirst()
    client = await Client.objects.filter(tg_chat_id=callback.from_user.id).afirst()
    balance_and_spending = await sync_to_async(lambda: client.balance)()
    full_name = await sync_to_async(lambda: client.full_name)()
    greeting = await retrieve_greeting(full_name)
    if not balance_and_spending:
        text = await create_description(program)
        capture_message("Не удалось получить информацию о балансе и расходах клиента.")
        await callback.message.edit_text(
            text=text, reply_markup=await main_menu(bool(client.enote_id))
        )
        return
    balance, money_spent = balance_and_spending
    status = await program.retrieve_status(money_spent)
    balance_msg = f"Баланс Вашего бонусного счета: {balance} бонусных баллов.\n\n{program.description}"
    if status:
        msg = (
            f"на данный момент Ваш статус в программе лояльности:\n\n<b>{status.name}</b>\n\nЭто "
            f"значит, что Вы получаете {status.cashback_amount}% бонусными баллами с потраченной "
            f"в Клинике суммы!\n\n{balance_msg}"
        )
    else:
        capture_message("Неправильно указаны интервалы статусов программ")
        msg = balance_msg
    await callback.message.edit_text(
        text=f"{greeting} {msg}",
        reply_markup=await bonuses_menu(),
    )


@bonuses_router.callback_query(F.data == "loyalty")
async def loyalty_program(callback: types.CallbackQuery):
    client = await Client.objects.filter(tg_chat_id=callback.from_user.id).afirst()
    program = await Program.objects.filter(is_active=True).afirst()
    text = await create_description(program)
    statuses = await sync_to_async(list)(program.statuses.order_by("start_amount"))
    reply_markup = await back_to_menu()
    if client.enote_id:
        reply_markup = await back_to_bonuses()
    for status in statuses:
        if status.end_amount:
            text += (
                f"\n\n<b>{status.name} статус</b> - кешбэк {status.cashback_amount}%\n<i>Клиент "
                f"оплатил услуг Клиники на {status.start_amount} - {status.end_amount} руб</i>"
            )
        else:
            text += (
                f"\n\n<b>{status.name} статус</b> - кешбэк {status.cashback_amount}%\n<i>Клиент "
                f"оплатил услуг Клиники на {status.start_amount} и больше руб</i>"
            )
    await callback.message.edit_text(
        text=f"{text}"
        f"\n\nКроме этого, Клиника подарит {program.new_client_bonus_amount} бонусных баллов за каждого нового Клиента, "
        "которому Вы рекомендовали нашу Клинику.",
        reply_markup=reply_markup,
    )


async def create_promocode() -> str:
    while True:
        promocode = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        is_unique = (
            await Recommendation.objects.filter(promocode=promocode).aexists() is False
        )
        if is_unique:
            return promocode


@bonuses_router.callback_query(
    F.data.in_({"recommend_from_bonuses", "recommend_from_menu"})
)
async def get_promocode(callback: types.CallbackQuery):
    promocode = await create_promocode()
    client = await Client.objects.aget(tg_chat_id=callback.from_user.id)
    program = await Program.objects.filter(is_active=True).afirst()
    await Recommendation.objects.acreate(promocode=promocode, client=client)
    full_name = await sync_to_async(lambda: client.full_name)()
    greeting = await retrieve_greeting(full_name)
    if callback.data == "recommend_from_menu":
        reply_markup = await back_to_menu()
    else:
        reply_markup = await back_to_bonuses()
    msg = (
        f"{greeting}мы безмерно ценим, когда нас рекомендуют!\n\nПоэтому мы начислим {program.new_client_bonus_amount} "
        f"бонусных баллов на Ваш счет в Клинике и {program.new_client_bonus_amount} приветственных баллов Вашему другу "
        "или родственнику в знак благодарности за каждого нашего будущего Клиента, "
        "которому Вы порекомендуете наш Центр. \n\nЧтобы рекомендовать нас,перешлите "
        "промокод клиенту, который собирается прийти в клинику ⤵️\n\nВаш промокод: "
        f"{promocode}"
    )
    await callback.message.edit_text(
        text=msg,
        reply_markup=reply_markup,
    )
