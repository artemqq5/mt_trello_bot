from telebot import types


def masons_partners_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Створити завдання 🪄', callback_data="masons_partners"))

    return markup