from ast import literal_eval

import requests
from aiogram import types
from trello import TrelloClient

from config.public_config import *
from constants.base import CREO


class TrelloManager:

    def __init__(self):
        self.__client = TrelloClient(
            api_key=API_KEY_TRELLO,
            api_secret=SECRET_TRELLO,
            token=TOKEN_TRELLO
        )

        self.__url_card = "https://api.trello.com/1/cards"
        self.__url_lebel = "https://api.trello.com/1/labels"
        self.__url_webhook = "https://api.trello.com/1/webhooks/"
        self.__default_body = {'key': API_KEY_TRELLO, 'token': TOKEN_TRELLO}

    def _create_label(self, name, _board):
        query = {
            'name': f'{name}',
            'color': 'black',
            'idBoard': ID_BOARD_CREO if _board == CREO else ID_BOARD_TECH
        }

        response = requests.request(
            "POST",
            url=self.__url_lebel,
            params=query | self.__default_body
        )

        return literal_eval(response.text)['id']

    def _create_card(self, card, labels, _list):
        query = {
            'idList': ID_LIST_CREO if _list == CREO else ID_LIST_TECH,
            'name': card.name,
            'desc': card.desc,
            'idLabels': labels,
            'due': card.date
        }

        return requests.request(
            "POST",
            url=self.__url_card,
            headers={"Accept": "application/json"},
            params=query | self.__default_body
        )

    def _add_attachments_card(self, card_id, source):
        for i in source:
            query = {
                'url': i
            }

            requests.request(
                "POST",
                url=f"https://api.trello.com/1/cards/{card_id}/attachments",
                headers={"Accept": "application/json"},
                params=query | self.__default_body
            )

    def _get_tasks(self, _list, user_label):
        card_list = ID_LIST_CREO if _list == CREO else ID_LIST_TECH
        tasks_l = self.__client.get_list(card_list).list_cards()

        markup = types.InlineKeyboardMarkup()
        for card in tasks_l:
            for label in card.idLabels:
                if str(label) == user_label:
                    markup.add(types.InlineKeyboardButton(card.name, callback_data=f"card_{card.id}"))

        return markup

    def _get_callback_cards(self):
        list_callback = []
        try:
            tech_tasks = self.__client.get_list(ID_LIST_TECH).list_cards()
            creo_tasks = self.__client.get_list(ID_LIST_CREO).list_cards()
            tasks_l = tech_tasks + creo_tasks
            for card in tasks_l:
                list_callback.append(f"card_{card.id}")
        except Exception as e:
            print(f"_get_callvack_cards_trello: {e}")
        finally:
            return list_callback

    def _get_card(self, id_card):
        card = self.__client.get_card(id_card)
        return card

    def _delete_card(self, id_card):
        return requests.request(
            "DELETE",
            url=self.__url_card + f"/{id_card}",
            headers={"Accept": "application/json"},
            params=self.__default_body
        )

    def _write_comment(self, id_card, text):
        comment_link = f"https://api.trello.com/1/cards/{id_card}/actions/comments"

        return requests.request(
            "POST",
            url=comment_link,
            headers={"Accept": "application/json"},
            params={'text': text} | self.__default_body
        )

    def _set_webhook_card(self, card_id, vertical):
        query = {
            'callbackURL': f'{HOSTENAME_}/webhook',
            'idModel': card_id,
            'description': f'{vertical}_webhook_card_{card_id}'
        }

        return requests.post(
            self.__url_webhook,
            headers={'Content-Type': 'application/json'},
            params=query | self.__default_body
        )
