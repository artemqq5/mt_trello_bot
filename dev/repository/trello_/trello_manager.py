import json
from ast import literal_eval

import requests
from aiogram import types
from trello import TrelloClient

from config.public_config import *
from constants.base import CREO


class TrelloManager:
    def _get_callback_cards(self):
        list_callback = []
        try:
            url_creo = f"https://api.trello.com/1/lists/{ID_LIST_CREO}/cards"
            url_tech = f"https://api.trello.com/1/lists/{ID_LIST_TECH}/cards"

            headers = {
                "Accept": "application/json"
            }

            query = {
                'key': API_KEY_TRELLO,
                'token': TOKEN_TRELLO
            }

            response_creo = requests.request(
                "GET",
                url_creo,
                headers=headers,
                params=query
            )

            response_tech = requests.request(
                "GET",
                url_tech,
                headers=headers,
                params=query
            )

            card_ids = [card['id'] for card in response_creo.json() + response_tech.json()]

            for card_id in card_ids:
                list_callback.append(f"card_{card_id}")
        except Exception as e:
            print(f"_get_callvack_cards_trello: {e}")
        finally:
            return list_callback

    def _get_card(self, id_card):
        return requests.request(
            "GET",
            url=self.__url_card + f"/{id_card}",
            headers={"Accept": "application/json"},
            params=self.__default_body
        ).json()

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
