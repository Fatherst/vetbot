#from bot_admin.create_bot import bot, dp
from django.core.management.base import BaseCommand
from admin_auth.handlers import admin_router
from client_auth.handlers import client_router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv
import os


load_dotenv()

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
load_dotenv()
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
bot = Bot(BOT_API_TOKEN)
dp = Dispatcher(storage=storage)

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")
WEBHOOK_PATH = f"/{BOT_API_TOKEN}"
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")



async def on_startup(bot: Bot) -> None:
    print("Бот в онлайне")
    dp.include_router(admin_router)
    dp.include_router(client_router)
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def launch_bot():
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
       dispatcher=dp,
       bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST,port=WEB_SERVER_PORT)


class Command(BaseCommand):
    """
    Команда для запуска бота
    Запуск: python manage.py start_bot
    """

    help = "Bot start"

    def handle(self, *args, **options):
        launch_bot()
