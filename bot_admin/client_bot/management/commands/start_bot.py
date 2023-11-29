import sys
sys.path.append(".")
from bot_admin.create_bot import bot,dp
from client_bot.handlers import register_handlers_client
from admin_dialog.handlers import register_handlers_admin
from aiogram.utils import executor
from django.core.management.base import BaseCommand
register_handlers_admin(dp)
register_handlers_client(dp)

async def on_startup(_):
    print("Бот в онлайне")


class Command(BaseCommand):
    """
    Команда для запуска бота
    Запуск: python manage.py start_bot
    """
    help = 'Bot start'
    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)