from telebot import types


def tech_task_mode():
    markup = types.ReplyKeyboardMarkup()

    list_buttons = (
        types.KeyboardButton('Masons Partners'),
        types.KeyboardButton('Gambling FB'),
        types.KeyboardButton('Gambling PPC'),
        types.KeyboardButton('Gambling UAC'),
        types.KeyboardButton('AF Manager'),
    )

    for i in list_buttons:
        markup.add(i)

    return markup
