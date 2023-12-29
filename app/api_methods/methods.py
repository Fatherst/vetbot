import aiohttp
from django.conf import settings
from aiohttp.client_exceptions import ClientResponseError
from client_auth.models import Client
import logging


logger = logging.getLogger(__name__)


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
                settings.ENOTE_API_URL + "balance",
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


async def easy_send_code(code: int, phone_number):
    query_params = {
        "login": settings.EASY_LOGIN,
        "password": settings.EASY_PASSWORD,
        "text": f"Твой код - {code}",
        "originator": settings.EASY_ORIGINATOR,
        "department_enote_id": settings.ENOTE_BALANCE_DEPARTMENT,
        "phone": phone_number,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://xml.smstec.ru/api/v1/easysms/{settings.EASY_ID}/send_sms",
                params=query_params,
            ) as resp:
                resp.raise_for_status()
                print(resp)
                text = await resp.text()
                print(text)
                if text.__contains__("ERROR"):
                    return False
                return True
    except Exception as error:
        logger.error(error)
        print(error)
        return error
