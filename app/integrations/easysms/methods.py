import requests
from django.conf import settings


def send_message(message: str, phone: str):
    params = {
        "login": settings.EASYSMS_LOGIN,
        "password": settings.EASYSMS_PASSWORD,
        "text": message,
        "originator": settings.EASYSMS_ORIGINATOR,
        "phone": phone,
    }
    response = requests.get(url=f"{settings.EASYSMS_URL}/send_sms", params=params)
    response.raise_for_status()

    text = response.text
    if "ERROR" in text:
        raise Exception(f"Problems with easysms: {text}")
