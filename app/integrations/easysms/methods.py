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
        "department_enote_id": settings.ENOTE_BALANCE_DEPARTMENT,
        "phone": phone_number,
    }
    try:
        async with (aiohttp.ClientSession() as session):
            async with session.get(
                settings.EASY_SEND_SMS_URL,
                params=query_params,
            ) as resp:
                resp.raise_for_status()
                text = await resp.text()
                if (
                    text.__contains__("ERROR: Error code: 91")
                    or text.__contains__("ERROR: Error code: 46")
                    or text.__contains__("ERROR: Error code: 66")
                    or text.__contains__("ERROR: Error code: 61")
                ):
                    return False
                return True
    except Exception as error:
        logger.error(error)
        return error
