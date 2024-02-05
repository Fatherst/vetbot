import logging
from aiogram import Router, F
from aiogram import types
from asgiref.sync import sync_to_async
from django.db.models import Q
from .keyboards import (
    back_to_bonuses_or_menu,
    bonuses_menu,
)
from client_auth.models import Client
from bonuses.models import Status, Program, BonusAccrual
from sentry_sdk import capture_message


logger = logging.getLogger(__name__)


bonuses_router = Router()


@bonuses_router.callback_query(F.data == "bonuses")
async def bonuses_program(callback: types.CallbackQuery):
    client = await Client.objects.filter(tg_chat_id=callback.from_user.id).afirst()
    # balance = await get_balance(client)
    # money_spent = balance.clientPrepaid
    balance = 5
    money_spent = 100
    program = await Program.objects.filter(is_active=True).afirst()
    status = await program.statuses.filter(
        Q(start_amount__lte=money_spent)
        & (Q(end_amount__gte=money_spent) | Q(end_amount__isnull=True))
    ).afirst()
    if status:
        msg = (
            (
                f"на данный момент Ваш статус в программе лояльности:\n\n<b>{status.name}</b>\n\nЭто "
                f"значит, что Вы получаете {status.cashback_amount}% бонусными баллами с потраченной "
                f"в Клинике суммы!\n\nБаланс Вашего бонусного счета:"
                f" {balance} бонусных баллов.\n\n{program.description}"
            )
            if balance
            else "к сожалению, у вас пока нет бонусного счёта, вы сможете открыть его при посещении клиники"
        )
    else:
        capture_message("Неправильно указаны интервалы статусов программ")
        msg = f"Баланс Вашего бонусного счета: {balance} бонусных баллов.\n\n{program.description}"
    await callback.message.edit_text(
        text=f"<b>{callback.from_user.first_name}</b>, {msg}",
        reply_markup=await bonuses_menu(bool(balance)),
    )


@bonuses_router.callback_query(F.data == "loyalty")
async def loyalty_program(callback: types.CallbackQuery):
    client = await Client.objects.filter(tg_chat_id=callback.from_user.id).afirst()
    program = await Program.objects.filter(is_active=True).afirst()
    statuses = await sync_to_async(list)(program.statuses.order_by("start_amount"))
    text = "В рамках программы лояльности Клиника начисляет Клиентам бонусные баллы (кешбэк), которые можно"
    f" использовать для оплаты услуг Клиники.\n\n{program.description}\n\nРазмер кешбэка зависит от статуса"
    " Клиента в программе лояльности:"
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
        reply_markup=await back_to_bonuses_or_menu(bool(client.enote_id)),
    )
