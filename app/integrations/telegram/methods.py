import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_message(chat_id: int, text: str):
    try:
        requests.get(
            f"https://api.telegram.org/bot{settings.BOT_API_TOKEN}/sendMessage",
            params={
                "chat_id": chat_id,
                "text": text,
            },
        )
    except Exception as error:
        logger.error(error)
