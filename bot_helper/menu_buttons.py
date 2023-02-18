from telebot import types


def setStartButton():
    markup = types.ReplyKeyboardMarkup()

    listButtons = (
        types.KeyboardButton('Gambling FB (В разработке)'),
        types.KeyboardButton('Gambling PPC (В разработке)'),
        types.KeyboardButton('Gambling UAC (В разработке)'),
        types.KeyboardButton('AF Manager'),
        types.KeyboardButton('Schema (В разработке)'),
    )

    for i in listButtons:
        markup.add(i)

    return markup


def af_manager_menu():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Редактировать оффер', callback_data="edit_offer"),
        types.InlineKeyboardButton('Добавить оффер', callback_data="add_offer"),
    )

    for i in listButtons:
        markup.add(i)

    return markup


def choice_offer_type():
    markup = types.ReplyKeyboardMarkup()

    markup.add(types.KeyboardButton('Новый'))
    markup.add(types.KeyboardButton('Существующий'))

    return markup
