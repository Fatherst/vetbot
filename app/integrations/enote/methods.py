import json
import logging
import aiohttp
import requests
from django.conf import settings
from aiohttp.client_exceptions import ClientResponseError
from client_auth.models import Client
from bonuses.models import BonusAccrual

logger = logging.getLogger(__name__)


def add_bonus_points(bonus: BonusAccrual):
    data = {
        "discountOperationType": "ADD",
        "departmentEnoteId": settings.ENOTE_BALANCE_DEPARTMENT,
        "description": bonus.reason,
        "bonusPoints": [
            {
                "discountCardEnoteId": "a6867c31-cf7b-4e1e-92de-9f521a41392a",
                "eventDate": str(bonus.created_at),
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
