from telebot.handler_backends import BaseMiddleware, SkipHandler, ContinueHandling
import client_auth.models as models
from telebot import types


class Middleware(BaseMiddleware):
    def __init__(self, bot):
        self.bot = bot
        self.update_types = ["message", "callback_query"]

    def send_message_to_blocked_client(self, chat_id, message_id):
        text = (
            "Здравствуйте! Благодарим за обращение. На данный момент услуга недоступна."
        )
        if message_id:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
            return
        self.bot.send_message(chat_id=chat_id, text=text)

    def pre_process(self, message, data):
        message_id = None
        if type(message) == types.Message:
            tg_id = message.chat.id
        if type(message) == types.CallbackQuery:
            tg_id = message.message.chat.id
            message_id = message.message.message_id
        if models.Client.objects.filter(tg_chat_id=tg_id).first().in_blacklist.exists():
            self.send_message_to_blocked_client(tg_id, message_id)
            return SkipHandler()
        else:
            return ContinueHandling()
