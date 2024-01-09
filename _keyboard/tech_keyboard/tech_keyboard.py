from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from constants.base import CANCEL
from constants.tech import *


def tech_format_keyboard(dep) -> ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup()

    markup.add(KeyboardButton(CANCEL))

    for task in TECH_DEP_TASK[dep]:
        markup.add(KeyboardButton(task))

    return markup


def tech_advertiser_type_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup()

    markup.add(KeyboardButton(TYPE_TECH_NEW))
    markup.add(KeyboardButton(TYPE_TECH_EXIST))
    markup.add(KeyboardButton(CANCEL))

    return markup


