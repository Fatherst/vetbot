import logging
import time

import telebot
from bot.filters import PhoneFilter
from django.conf import settings
from telebot.custom_filters import StateFilter
from telebot.storage import StateRedisStorage


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBot(telebot.TeleBot, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        TOKEN = settings.BOT_TOKEN
        WEBHOOK_URL = settings.BOT_WEBHOOK

        state_storage = StateRedisStorage(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT
        )
        super().__init__(
            TOKEN, *args, state_storage=state_storage, parse_mode="HTML", **kwargs
        )

        self.remove_webhook()
        time.sleep(0.5)
        self.set_webhook(url=f"{WEBHOOK_URL}/webhook")

        self.add_custom_filter(StateFilter(self))
        self.add_custom_filter(PhoneFilter())


logger = telebot.logger
logger.setLevel(logging.DEBUG)

bot = SingletonBot()
