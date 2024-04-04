from telebot.handler_backends import BaseMiddleware
import client_auth.models as models
import client_auth.handlers as handlers

class Middleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ["message", "data"]

    def pre_process(self, message, data):
        tg_id = message.chat.id
        if models.Client.objects.filter(tg_chat_id=tg_id).first().in_blacklist.exists():
            handlers.send_message_to_blocked_user(message)
        else:
            pass
