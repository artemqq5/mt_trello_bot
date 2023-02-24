import datetime

from telebot import types


def setStartButton():
    markup = types.ReplyKeyboardMarkup()

    listButtons = (
        # types.KeyboardButton('Gambling FB (В разработке)'),
        # types.KeyboardButton('Gambling PPC (В разработке)'),
        # types.KeyboardButton('Gambling UAC (В разработке)'),
        types.KeyboardButton('AF Manager'),
        types.KeyboardButton('Media'),
        # types.KeyboardButton('Schema (В разработке)'),
    )

    for i in listButtons:
        markup.add(i)

    return markup


# =================AF Manager====================
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


# ==================AF Manager end===================


# ===============Media======================
def media_menu():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Заказать Креатив', callback_data="order_creative"))

    return markup


def choice_media_type_date():
    markup = types.ReplyKeyboardMarkup()

    markup.add(types.KeyboardButton('Пропустить'))

    markup.row(
        types.KeyboardButton('Сегодня 12:00'),
        types.KeyboardButton('Сегодня 15:00'),
        types.KeyboardButton('Сегодня 18:00'),
    )
    markup.row(
        types.KeyboardButton('Завтра 12:00'),
        types.KeyboardButton('Завтра 15:00'),
        types.KeyboardButton('Завтра 18:00'),
    )

    return markup
# ===============Media end======================
