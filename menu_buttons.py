from telebot import types


def setStartButton():
    markup = types.ReplyKeyboardMarkup()

    listButtons = (
        types.KeyboardButton('Gambling FB'),
        types.KeyboardButton('Gambling PPC'),
        types.KeyboardButton('Gambling UAC'),
        types.KeyboardButton('AF Manager'),
        types.KeyboardButton('Schema'),
        # types.KeyboardButton('Создать карточку'),
    )

    for i in listButtons:
        markup.add(i)

    return markup
