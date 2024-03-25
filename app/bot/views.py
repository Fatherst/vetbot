import telebot
from bot.bot_init import bot, logger
from client_auth.handlers import *
from bonuses.handlers import *
from appointment.handlers import *
from admin_auth.handlers import *
from nps.handlers import *
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook(request: HttpRequest):
    if request.method == "POST":
        update = request.body.decode("utf-8")
        logger.info(update)
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return HttpResponse("<h1>Welcome to Vet Bot!</h1>")
