from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

storage = MemoryStorage()
API_TOKEN = '6936825219:AAGPrV2WXZvMbz_bYQjzcqv9ylfj2kI3IoE'
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=storage)


