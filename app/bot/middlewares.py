from telebot.handler_backends import BaseMiddleware
import client_auth.models as models


class Middleware(BaseMiddleware):
    def __init__(self, bot):
        self.bot = bot
        self.update_types = ["message", "data"]

    def send_message_to_blocked_client(self, message_id):
        text = "Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна."
        self.bot.send_message(chat_id=message_id, text=text)
    def pre_process(self, message, data):
        print(self.bot)
        tg_id = message.chat.id
        if models.Client.objects.filter(tg_chat_id=tg_id).first().in_blacklist.exists():
            self.send_message_to_blocked_client(tg_id)
            return
        else:
            pass
