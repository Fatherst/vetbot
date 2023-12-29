from aiogram import types
from .keyboards import (
    back_to_bonuses,
    bonuses_menu,
)
from client_auth.models import Client
from aiogram import Router, F
from api_methods.methods import get_balance
import logging


logger = logging.getLogger(__name__)


bonuses_router = Router()


@bonuses_router.callback_query(F.data == "bonuses")
async def bonuses_program(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    client = await Client.objects.filter(tg_chat_id=user_id).afirst()
    balance = await get_balance(client)
    msg = (
        (
            f"на данный момент Ваш статус в программе лояльности:\n\n<b>БРОНЗОВЫЙ</b>\n\nЭто значит,"
            f" что Вы получаете"
            f" 3% бонусными баллами с потраченной в Клинике суммы!\n\nБаланс Вашего бонусного счета:"
            f" {balance} бонусных баллов.\n\nВы можете оплатить бонусами до 20% от стоимости услуг"
            f" Клиники!\n\n1 бонусный балл = 1 рубль"
        )
        if balance
        else "к сожалению, у вас пока нет бонусного счёта, вы сможете открыть его при посещении клиники"
    )
    await callback.message.edit_text(
        text=f"<b>{callback.from_user.first_name}</b>, {msg}",
        reply_markup=await bonuses_menu(bool(balance)),
    )


@bonuses_router.callback_query(F.data == "loyalty")
async def loyalty_program(callback: types.CallbackQuery):
    client = await Client.objects.filter(tg_chat_id=callback.from_user.id).afirst()
    await callback.message.edit_text(
        text="В рамках программы лояльности Клиника начисляет Клиентам бонусные баллы (кешбэк), которые можно"
        " использовать для оплаты услуг Клиники.\n\n 1 бонусный балл = 1 рубль\n\nРазмер кешбэка зависит от статуса"
        " Клиента в программе лояльности:\n\nБронзовый статус - кешбэк 3%\n\nКлиент оплатил услуг Клиники "
        "на 0 - 9999 руб\n\nСеребряный статус - кешбэк 5%\n\nКлиент оплатил услуг Клиники на 10000 - 29999 руб"
        "\n\nЗолотой статус - кешбэк 8%\n\nКлиент оплатил услуг Клиники на 30000 - 49999 руб\n\n"
        "Платиновый статус - кешбэк 10%\n\nКлиент оплатил услуг Клиники на сумму более 50000 руб\n\n"
        "Вы можете оплатить бонусами до 10% стоимости услуг хирургии и до 20% от стоимости услуг терапии Клиники!"
        "\n\nКроме этого, Клиника подарит 1000 бонусных баллов за каждого нового Клиента, "
        "которому Вы рекомендовали нашу Клинику.",
        reply_markup=await back_to_bonuses(bool(client.enote_id)),
    )
