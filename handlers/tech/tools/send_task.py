import datetime

from _keyboard.base_keyboard import menu_keyboard
from config.public_config import card_labels_creo, card_labels_tech
from constants.base import MESSAGE_SEND, MESSAGE_DONT_SEND, TECH
from constants.dep import ADMIN_
from handlers.creo.tools.message_tools import parse_to_trello_card_format_creo
from handlers.creo.tools.notify_creo import notify_new_creo
from handlers.tech.tools.message_tools import parse_to_trello_card_format_tech
from handlers.tech.tools.notify_tech import notify_new_tech
from repository.card_repository.card_repos import CardRepository
from repository.model.card_creo import CardModelCreo
from repository.model.card_creo import CardModelCreo
from repository.model.card_tech import CardModelTech
from repository.trello_.trello_repository import TrelloRepository
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


async def send_order_tech(data, message, type_):
    if data is not None:
        user = get_user_model(UserRepository().get_user(message.chat.id))
        try:
            add_task_db = CardRepository().add_card_tech(CardModelTech(
                name=f"{type_} by ({user.name})",
                date=datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
                id_user=user.id,
                id_card=None,
                url_card=None,
            ))
        except Exception as e:
            print(f"send_order_tech: {e}")
            add_task_db = None

        if add_task_db is not None:
            trello_card = parse_to_trello_card_format_tech(id_=add_task_db, task_tech=data, task_type=type_, user=user, user_tg=message.chat.username)
            add_terello = TrelloRepository().create_card_tech(trello_card, [user.label_tech, card_labels_tech[user.dep]])
            if add_terello is not None:
                json_card = add_terello.json()
                TrelloRepository().set_webhook(json_card['id'], TECH)  # set webhook
                CardRepository().update_card_tech(card_id_trello=json_card['id'], url_card=json_card['shortUrl'],
                                                  id_=add_task_db)
                await notify_new_tech(message, trello_card, json_card['shortUrl'])
                await message.answer(f"{MESSAGE_SEND}", reply_markup=menu_keyboard())
            else:
                await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
        else:
            await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
    else:
        await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
