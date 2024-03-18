import re

from telebot.custom_filters import SimpleCustomFilter
from telebot import types
from bot.classes import Phone


class PhoneFilter(SimpleCustomFilter):
    key = "phone_is_valid"

    def check(self, message: types.Message):
        if message.text:
            row_phone = message.text
        else:
            row_phone = message.contact.phone_number

        phone = Phone.format(row_phone)

        return Phone.validate(phone)
