import logging
import aiohttp
from django.conf import settings


logger = logging.getLogger(__name__)


async def easy_send_code(code: int, phone_number):
    query_params = {
        "login": settings.EASY_LOGIN,
        "password": settings.EASY_PASSWORD,
        "text": f"Твой код - {code}",
        "originator": settings.EASY_ORIGINATOR,
        "phone": phone_number,
    }
    try:
        async with (aiohttp.ClientSession() as session):
            async with session.get(
                f"{settings.EASY_API_URL}send_sms",
                params=query_params,
            ) as resp:
                resp.raise_for_status()
                text = await resp.text()
                if text.__contains__("ERROR"):
                    return False
                return True
    except Exception as error:
        logger.error(error)
        return False
