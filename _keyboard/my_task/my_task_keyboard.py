from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from constants.base import CANCEL
from constants.my_task import MY_CREO_TASK, MY_TECH_TASK, DELETE_TASK, COMMENT_TASK
from repository.card_repository.card_repos import CardRepository
from repository.trello_.trello_repository import TrelloRepository


def choose_tasks_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup()

    markup.add(KeyboardButton(MY_CREO_TASK))
    markup.add(KeyboardButton(MY_TECH_TASK))
    markup.add(KeyboardButton(CANCEL))

    return markup


def my_task_creo_callback_keyboard(user) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    all_cards = TrelloRepository().get_callback_cards()

    for card in all_cards:
        card_id = card.split("card_")[1]
        card_model = CardRepository().get_card_creo_by_card_id(card_id)
        if card_model is not None and card_model['id_user'] == user.id:
            name = f"# {card_model['id']} {card_model['name']}"
            keyboard.add(InlineKeyboardButton(text=name, callback_data=card))

    return keyboard


def my_task_tech_callback_keyboard(user) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    all_cards = TrelloRepository().get_callback_cards()

    for card in all_cards:
        card_id = card.split("card_")[1]
        card_model = CardRepository().get_card_tech_by_card_id(card_id)
        if card_model is not None and card_model['id_user'] == user.id:
            name = f"# {card_model['id']} {card_model['name']}"
            keyboard.add(InlineKeyboardButton(text=name, callback_data=card))

    return keyboard


def manage_task_keyboard(id_card):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=DELETE_TASK, callback_data=f"delete_{id_card}"))
    keyboard.add(InlineKeyboardButton(text=COMMENT_TASK, callback_data=f"comment_{id_card}"))

    return keyboard

