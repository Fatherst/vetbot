import logging
import aiohttp
from django.conf import settings
from aiohttp.client_exceptions import ClientResponseError
from client_auth.models import Client
from bonuses.models import BonusAccural


logger = logging.getLogger(__name__)


async def accrual_post(bonus: BonusAccural):
    print(bonus.client.enote_id)
    data = {
        "client_enote_id": bonus.client.enote_id,
        "department_enote_id": settings.ENOTE_BALANCE_DEPARTMENT,
    }
    headers = {
        "apikey": settings.ENOTE_APIKEY,
        "Authorization": settings.ENOTE_BASIC_AUTH,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.ENOTE_API_URL}/bonus_points",
                data=data,
                headers=headers,
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                return
    except ClientResponseError as error:
        logger.error(error)
        return


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
