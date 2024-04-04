from telebot.handler_backends import BaseMiddleware
import client_auth.models as models


class Middleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ["message", "data"]

    def pre_process(self, message, data):
        tg_id = message.chat.id
        if models.Client.objects.filter(tg_chat_id=tg_id).first().in_blacklist.exists():
            pass
        else:
            pass
