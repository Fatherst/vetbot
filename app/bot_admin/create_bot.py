from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
import logging
import sys
from django.conf import settings


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
load_dotenv()
bot = Bot(settings.BOT_API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)
