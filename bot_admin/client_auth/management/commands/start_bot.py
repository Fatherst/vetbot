import sys
sys.path.append(".")
from bot_admin.create_bot import bot,dp
from django.core.management.base import BaseCommand
from admin_auth import handlers as clr
from client_auth import handlers as adr
import asyncio
from aiogram import Bot
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import os


WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = "/6936825219:AAGPrV2WXZvMbz_bYQjzcqv9ylfj2kI3IoE"
BASE_WEBHOOK_URL = "https://4f94-2a00-a041-f49f-ffa8-8cff-3595-4971-b9df.ngrok-free.app"
WEBHOOK_SECRET = "my-secret"



async def on_startup(bot: Bot)->None:
    print("Бот в онлайне")
    dp.include_router(clr.admin_router)
    dp.include_router(adr.client_router)
    await dp.start_polling(bot)
    #await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")#, secret_token=WEBHOOK_SECRET)

#def launch_bot():
    #app = web.Application()
    #webhook_requests_handler = SimpleRequestHandler(
    #    dispatcher=dp,
    #    bot=bot)
    #    secret_token=WEBHOOK_SECRET,
    #)
    #webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    #setup_application(app, dp, bot=bot)
    #web.run_app(app, host=WEB_SERVER_HOST,port=WEB_SERVER_PORT)

class Command(BaseCommand):
    """
    Команда для запуска бота
    Запуск: python manage.py start_bot
    """
    help = 'Bot start'
    def handle(self, *args, **options):
        #launch_bot()
        asyncio.run(on_startup(bot))