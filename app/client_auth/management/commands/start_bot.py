import asyncio
import logging

from admin_auth.handlers import admin_router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from client_auth.handlers import client_router
from django.conf import settings
from django.core.management.base import BaseCommand


async def launch_bot():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(settings.BOT_API_TOKEN, parse_mode="HTML")

    dp.include_router(admin_router)
    dp.include_router(client_router)

    await bot.delete_webhook()
    await dp.start_polling(bot)

    logging.info("Бот в онлайне")


class Command(BaseCommand):
    """
    Команда для запуска бота
    Запуск: python manage.py start_bot
    """

    help = "Bot start"

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        asyncio.run(launch_bot())
