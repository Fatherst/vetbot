import json
import logging
import aiohttp
from django.conf import settings
from aiohttp.client_exceptions import ClientResponseError
from client_auth.models import Client
from bonuses.models import BonusAccrual


logger = logging.getLogger(__name__)


async def accrual_enote(bonus: BonusAccrual):
    data = {
        "discountOperationType": "ADD",
        "departmentEnoteId": "14bc1738-5781-43f7-9b6d-3b1a9769fc9d",
        "description": "Тест",
        "bonusPoints": [
            {
                "discountCardEnoteId": "a6867c31-cf7b-4e1e-92de-9f521a41392a",
                "eventDate": f"{bonus.modified_at}" if bonus.modified_at else f"{bonus.created_at}",
                "sum": bonus.amount,
            }
        ],
    }
    json_data = json.dumps(data)
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.ENOTE_API_URL}/bonus_points",
                data=json_data,
                headers=headers,
            ) as resp:
                body = await resp.json()
                resp.raise_for_status()
                return True
    except ClientResponseError as error:
        logger.error(error)
        return False


async def get_balance(client: Client):
    query_params = {
        "client_enote_id": client.enote_id,
        "department_enote_id": settings.ENOTE_BALANCE_DEPARTMENT,
    }
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }
    balance = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.ENOTE_API_URL}/balance",
                params=query_params,
                headers=headers,
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                balance = body["clientBonusPoints"]
                return balance
    except ClientResponseError as error:
        logger.error(error)
        return balance
