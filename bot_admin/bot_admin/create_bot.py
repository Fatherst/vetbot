from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
import logging
import sys


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
load_dotenv()
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
bot = Bot(BOT_API_TOKEN)
dp = Dispatcher(storage=storage)
