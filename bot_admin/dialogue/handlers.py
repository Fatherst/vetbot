import sys

sys.path.append(".")
from bot_admin.create_bot import bot, dp
from aiogram import types, Dispatcher

# from .keyboards import (

# )
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re
import random
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from aiogram import Router, F
from aiogram.filters import Command


dialogue_router = Router()
