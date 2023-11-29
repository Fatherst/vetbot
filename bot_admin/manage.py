#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import multiprocessing
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_admin.settings")
django.setup()
from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from multiprocessing import Process
from admin_dialog import views
from admin_dialog.create_bot import bot, dp
import threading


views.register_handlers_client(dp)


async def on_startup(_):
    print("Бот в онлайне")


def launch_bot():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_admin.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    """Костыль: пытается вызвать несколько экземпляров бота
    Решение:"""
    p2 = multiprocessing.Process(target=launch_bot)
    p2.start()
    p1 = multiprocessing.Process(target=main)
    p1.start()
