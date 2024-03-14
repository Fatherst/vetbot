import re

from telebot.custom_filters import SimpleCustomFilter
from telebot import types


class PhoneFilter(SimpleCustomFilter):
    key = "phone_is_valid"

    def check(self, message: types.Message):
        if message.text:
            row_phone = message.text
        else:
            row_phone = message.contact.phone_number

        phone = re.sub(r"\D", "", row_phone)

        ru_phone_mask = r"([78][0-9]{10})"
        mask = re.compile(ru_phone_mask)

        return bool(re.fullmatch(mask, phone))
