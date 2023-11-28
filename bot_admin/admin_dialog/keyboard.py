from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_startinline_client():
    start_inline_client = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton('🆔 Пройти идентификацию', callback_data='1')
    start_inline_client.add(b1)
    return start_inline_client

def get_identification():
    identification_markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton('Поделиться 🔗', callback_data='share')
    b2 = InlineKeyboardButton('Написать', callback_data='write')
    identification_markup.row(b1).add(b2)
    return identification_markup

def get_contact():
    contact_markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    b1 = KeyboardButton('Отослать номер',request_contact=True)
    contact_markup.add(b1)
    return contact_markup

def get_user_received_from_db():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton('Мои бонусы 💰',callback_data='bonuses')
    b2 = KeyboardButton('Мои записи 📝',callback_data='appointments')
    b3 = KeyboardButton('Записаться ✔️',callback_data='book')
    b4 = KeyboardButton('Рекомендовать клинику 📢',callback_data='recommend')
    b5 = KeyboardButton('О клинике  🛈',callback_data='about')
    b6 = KeyboardButton('Наши врачи 👩‍⚕️',callback_data='doctors')
    inline_markup.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)
    return inline_markup

def get_user_not_in_db():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton('О клинике  🛈', callback_data='about')
    b2 = KeyboardButton('Наши врачи 👩‍⚕️', callback_data='doctors')
    b3 = KeyboardButton('Программа лояльности 🐱', callback_data='loyalty')
    inline_markup.add(b1).add(b2).add(b3)
    return inline_markup

def get_new_appointment():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton('Мои бонусы 💰', callback_data='bonuses')
    b2 = KeyboardButton('Мои записи 📝', callback_data='appointments')
    b4 = KeyboardButton('Рекомендовать клинику 📢', callback_data='recommend')
    b5 = KeyboardButton('О клинике  🛈', callback_data='about')
    b6 = KeyboardButton('Наши врачи 👩‍⚕️', callback_data='doctors')
    b3 = KeyboardButton('Назад 🔙', callback_data='back')
    inline_markup.add(b1).add(b2).add(b4).add(b5).add(b6).add(b3)
    return inline_markup

def get_admin_code():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    b1 = KeyboardButton('Получить код', callback_data='admin_email')
    inline_markup.add(b1)
    return inline_markup