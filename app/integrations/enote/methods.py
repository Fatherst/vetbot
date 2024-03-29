import json

import requests
from bot.bot_init import logger
from django.conf import settings
from ninja import schema


class ClientBalance(schema.BaseModel):
    bonus_balance: int
    money_spent: int


def add_bonus_points(
    discount_card_enote_id: str, reason: str, amount: int, created_at: str
) -> bool:
    data = {
        "discountOperationType": "ADD",
        "departmentEnoteId": settings.ENOTE_BALANCE_DEPARTMENT,
        "description": reason,
        "bonusPoints": [
            {
                "discountCardEnoteId": discount_card_enote_id,
                "eventDate": created_at,
                "sum": amount,
            }
        ],
    }
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }
    response = requests.post(
        url=f"{settings.ENOTE_API_URL}/bonus_points",
        headers=headers,
        data=json.dumps(data),
    )
    try:
        response.raise_for_status()
    except Exception as e:
        logger.exception(e)
        return False

    return True


def get_balance(client_enote_id: str, card_enote_id: str) -> ClientBalance:
    query_params = {
        "client_enote_id": client_enote_id,
        "department_enote_id": settings.ENOTE_BALANCE_DEPARTMENT,
        "discount_card_enote_id": card_enote_id,
    }
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }

    response = requests.get(
        url=f"{settings.ENOTE_API_URL}/balance",
        params=query_params,
        headers=headers,
    )
    money_spent = 0
    bonus_balance = 0
    try:
        response.raise_for_status()
        body = response.json()
        income_1 = body["totalClientIncome"][0]
        income_2 = body["totalClientIncome"][1]
        if income_1["paymentMethod"] == "BONUS":
            money_spent = income_2["total"]
        else:
            money_spent = income_1["total"]
        bonus_balance = body["discountCardsBalances"][0]["total"]
    except Exception as e:
        logger.exception(e)

    return ClientBalance(bonus_balance=bonus_balance, money_spent=money_spent)
