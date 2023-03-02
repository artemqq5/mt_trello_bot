import datetime

from telebot import types


def setStartButton():
    markup = types.ReplyKeyboardMarkup()

    listButtons = (
        types.KeyboardButton('Мои Задания 📋'),
        types.KeyboardButton('Gambling FB'),
        types.KeyboardButton('Gambling PPC'),
        types.KeyboardButton('Gambling UAC'),
        types.KeyboardButton('AF Manager'),
        types.KeyboardButton('Media'),
    )

    for i in listButtons:
        markup.add(i)

    return markup


def my_tasks_menu():
    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton('tech', callback_data="my_task_tech"),
        types.InlineKeyboardButton('creo', callback_data="my_task_creo")
    )

    return markup


def manage_card():
    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton('Удалить задание', callback_data="delete_card"),
        types.InlineKeyboardButton('Написать комментарий', callback_data="commend_card")
    )

    return markup


def choice_date():
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


def skip_desc():
    return types.ReplyKeyboardMarkup().add(types.KeyboardButton('Пропустить'))
