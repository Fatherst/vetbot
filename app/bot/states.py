from telebot.handler_backends import State, StatesGroup


class AuthStates(StatesGroup):
    phone = State()
    code = State()


class AdminAuthStates(StatesGroup):
    email = State()
    code = State()
