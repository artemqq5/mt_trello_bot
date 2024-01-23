import datetime

from _keyboard.base_keyboard import menu_keyboard
from config.public_config import card_labels_creo
from constants.base import MESSAGE_SEND, MESSAGE_DONT_SEND, CREO
from constants.dep import ADMIN_
from handlers.creo.tools.message_tools import parse_to_trello_card_format_creo
from handlers.creo.tools.notify_creo import notify_new_creo
from repository.card_repository.card_repos import CardRepository
from repository.model.card_creo import CardModelCreo
from repository.model.card_creo import CardModelCreo
from repository.trello_.trello_repository import TrelloRepository
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


async def send_order_creo(data, message):
    if data is not None:
        user = get_user_model(UserRepository().get_user(message.chat.id))
        try:
            add_task_db = CardRepository().add_card_creo(CardModelCreo(
                name=f"Order Creative by ({user.name})",
                date=datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
                id_user=user.id,
                id_card=None,
                url_card=None,
                format_=data['general']['format_creo'],
                type_=data['general']['type_creo'],
                category=data['general']['category_creo'],
                description=data['description'],
                geo=data.get('geo', None),
                language=data.get('language', None),
                currency=data.get('currency', None),
                format_res=data.get('format', None),
                offer=data.get('offer', None),
                voice=data.get('voice', None),
                source=data.get('source', None),
                deadline=data.get('deadline', ""),
                count=data['count'],
                sub_desc=data.get('sub_description', None)
            ))
        except Exception as e:
            print(f"send_order_creo: {e}")
            add_task_db = None

        if add_task_db is not None:
            try:
                task = CardRepository().get_card_creo(add_task_db)
                trello_card = parse_to_trello_card_format_creo(task, user, user_tg=message.chat.username)
                add_terello = TrelloRepository().create_card_creo(trello_card,
                                                                  [user.label_creo, card_labels_creo[user.dep]])
                if add_terello is not None:
                    json_card = add_terello.json()
                    TrelloRepository().set_webhook(json_card['id'], CREO)  # set webhook
                    CardRepository().update_card_creo(card_id_trello=json_card['id'], url_card=json_card['shortUrl'],
                                                      id_=add_task_db)
                    await notify_new_creo(message, trello_card, json_card['shortUrl'])
                    await message.answer(f"{MESSAGE_SEND}", reply_markup=menu_keyboard())
                else:
                    await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
            except Exception as e:
                print(f"error send_order_creo: {e}")
                await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
        else:
            await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
    else:
        await message.answer(MESSAGE_DONT_SEND, reply_markup=menu_keyboard())
