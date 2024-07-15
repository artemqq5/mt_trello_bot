from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from constants.base import *
from constants.dep import DEP_LIST


def menu_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup()

    markup.add(KeyboardButton(MY_TASK))
    markup.add(KeyboardButton(CREO))
    markup.add(KeyboardButton(TECH))

    return markup


def cancel_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton(CANCEL))

    return markup


def skip_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.add(KeyboardButton(text=SKIP))
    keyboard.add(KeyboardButton(text=CANCEL))

    return keyboard


def dep_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton(ALL_DEP))

    for dep in DEP_LIST:
        markup.add(KeyboardButton(dep))

    markup.add(KeyboardButton(CANCEL))

    return markup
