from telebot import types


def setStartButton():
    markup = types.ReplyKeyboardMarkup()

    listButtons = (
        types.KeyboardButton('Добавить пользователя ➕'),
        types.KeyboardButton('Удалить пользователя ➖'),
        # types.KeyboardButton('Создать карточку'),
    )

    for i in listButtons:
        markup.add(i)

    return markup
