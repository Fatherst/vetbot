from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
import logging
import sys


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(API_TOKEN)
dp = Dispatcher(storage=storage)

