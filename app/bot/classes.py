import re


class Phone:
    @staticmethod
    def format(phone):
        cleaned_phone = re.sub(r"\D", "", phone)
        formatted_phone = f"7{cleaned_phone[1:]}"
        return formatted_phone

    @staticmethod
    def validate(phone):
        ru_phone_mask = r"([78][0-9]{10})"
        mask = re.compile(ru_phone_mask)
        return bool(re.fullmatch(mask, phone))
