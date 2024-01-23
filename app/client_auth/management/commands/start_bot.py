import asyncio
import logging

from admin_auth.handlers import admin_router
from bonuses.handlers import bonuses_router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from client_auth.handlers import client_router
from django.conf import settings
from django.core.management.base import BaseCommand
from bot_admin.create_bot import bot


async def launch_bot():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    # bot = Bot(settings.BOT_API_TOKEN, parse_mode="HTML")

    dp.include_router(admin_router)
    dp.include_router(client_router)
    dp.include_router(bonuses_router)

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
        asyncio.run(launch_bot())
