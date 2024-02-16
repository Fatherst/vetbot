import json
import logging
import aiohttp
import requests
from django.conf import settings
from typing import Union
from aiohttp.client_exceptions import ClientResponseError

logger = logging.getLogger(__name__)


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
    json_data = json.dumps(data)
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }
    try:
        resp = requests.post(
            url=f"{settings.ENOTE_API_URL}/bonus_points",
            headers=headers,
            data=json_data,
        )
        resp.raise_for_status()
        return True
    except ClientResponseError as error:
        logger.error(error)
        return False


async def get_balance(client_enote_id) -> Union[tuple, bool]:
    query_params = {
        "client_enote_id": client_enote_id,
        "department_enote_id": settings.ENOTE_BALANCE_DEPARTMENT,
    }
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.ENOTE_API_URL}/balance",
                params=query_params,
                headers=headers,
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                income_1 = body["totalClientIncome"][0]
                income_2 = body["totalClientIncome"][1]
                if income_1["paymentMethod"] == "BONUS":
                    bonus_balance = income_1["total"]
                    money_balance = income_2["total"]
                else:
                    bonus_balance = income_2["total"]
                    money_balance = income_1["total"]
                return (bonus_balance, money_balance)
    except ClientResponseError as error:
        logger.error(error)
        return False
