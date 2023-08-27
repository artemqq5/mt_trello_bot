from telebot import types


def creative_task_mode():
    markup = types.ReplyKeyboardMarkup()

    list_buttons = (
        types.KeyboardButton('Gambling Creo'),
        types.KeyboardButton('Crypto Creo'),
        types.KeyboardButton('Media or Other'),
    )

    for i in list_buttons:
        markup.add(i)

    return markup


def plash_google_apple():
    markup = types.ReplyKeyboardMarkup()

    markup.row(types.KeyboardButton('Google'), types.KeyboardButton('Apple'))
    markup.add(types.KeyboardButton('Google и Apple'))

    return markup
