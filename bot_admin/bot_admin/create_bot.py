from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=storage)
