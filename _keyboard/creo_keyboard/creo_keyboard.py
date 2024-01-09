from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from constants.base import CANCEL
from constants.creo import FORMAT_CREO_LIST, TYPE_CREO_LIST, FINANCE_CATEGORY_LIST, APP_STORE_TYPE, GOOGLE_PLAY_TYPE, \
    ALL_TASK_GOOD, ORDER_AGAIN_RETURN


def design_format_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for i in FORMAT_CREO_LIST:
        keyboard.add(KeyboardButton(text=i))

    keyboard.add(KeyboardButton(CANCEL))  # cancel button

    return keyboard


def design_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for i in TYPE_CREO_LIST:
        keyboard.add(KeyboardButton(text=i))

    keyboard.add(KeyboardButton(CANCEL))  # cancel button

    return keyboard


def design_category_keyboard(category_creo_list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for category in category_creo_list:
        keyboard.add(InlineKeyboardButton(text=category, callback_data=category))

    return keyboard


def design_category_finance_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for i in FINANCE_CATEGORY_LIST:
        keyboard.add(InlineKeyboardButton(text=i, callback_data=i))

    return keyboard


def design_app_platform_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.add(KeyboardButton(APP_STORE_TYPE))
    keyboard.add(KeyboardButton(GOOGLE_PLAY_TYPE))
    keyboard.add(KeyboardButton(CANCEL))  # cancel button

    return keyboard


def check_task_view_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.add(KeyboardButton(ALL_TASK_GOOD))
    keyboard.add(KeyboardButton(ORDER_AGAIN_RETURN))
    keyboard.add(KeyboardButton(CANCEL))  # cancel button

    return keyboard

