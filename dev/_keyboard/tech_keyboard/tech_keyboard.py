from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from constants.base import CANCEL
from constants.tech import *


def tech_format_keyboard(dep) -> ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton(CANCEL))

    for task in TECH_DEP_TASK[dep]:
        markup.add(KeyboardButton(task))

    return markup


def tech_advertiser_type_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton(TYPE_TECH_NEW))
    markup.add(KeyboardButton(TYPE_TECH_EXIST))
    markup.add(KeyboardButton(CANCEL))

    return markup


tech_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=GLEB_TECH, callback_data="ChoiceTechTask:gleb")],
    [InlineKeyboardButton(text=EGOR_TECH, callback_data="ChoiceTechTask:egor")]
])


