from ast import literal_eval

import requests

from private_config import API_KEY_TRELLO, TOKEN_TRELLO, HOSTENAME_


class TrelloManager:

    def __init__(self):
        self.__url_card = "https://api.trello.com/1/cards"
        self.__url_lebel = "https://api.trello.com/1/labels"
        self.__url_webhook = "https://api.trello.com/1/webhooks/"
        self.__default_body = {'key': API_KEY_TRELLO, 'token': TOKEN_TRELLO}

    # CREATE LABEL
    def _create_label(self, username, board_id):
        query = {'name': f'{username}', 'color': 'black', 'idBoard': board_id}
        response = requests.request("POST", url=self.__url_lebel, params=query | self.__default_body)
        return literal_eval(response.text)['id']

    # CREATE CARD
    def _create_card(self, card_name, card_desc, card_date, labels, list_id):
        query = {'idList': list_id, 'name': card_name, 'desc': card_desc, 'idLabels': labels, 'due': card_date}
        return requests.request(
            "POST", url=self.__url_card,
            headers={"Accept": "application/json"},
            params=query | self.__default_body
        )

    # CREATE WEBHOOK CARD
    def _set_webhook_card(self, card_id):
        query = {'callbackURL': f'{HOSTENAME_}', 'idModel': card_id, 'description': f'webhook_card_{card_id}'}
        return requests.post(
            self.__url_webhook,
            headers={'Content-Type': 'application/json'},
            params=query | self.__default_body
        )
