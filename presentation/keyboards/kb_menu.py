from aiogram_i18n import L
from aiogram_i18n.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu_all = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=L.MY_TASK())],
    [KeyboardButton(text=L.TASK_CREO()), KeyboardButton(text=L.TASK_AFF()), KeyboardButton(text=L.TASK_TECH())],
], resize_keyboard=True)

kb_menu_design_tech = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=L.MY_TASK())],
    [KeyboardButton(text=L.TASK_CREO()), KeyboardButton(text=L.TASK_TECH())],
], resize_keyboard=True)

kb_menu_design = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=L.MY_TASK())],
    [KeyboardButton(text=L.TASK_CREO())],
], resize_keyboard=True)

kb_menu_tech = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=L.MY_TASK())],
    [KeyboardButton(text=L.TASK_TECH())],
], resize_keyboard=True)