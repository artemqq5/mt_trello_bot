from ast import literal_eval

import requests

from private_config import API_KEY_TRELLO, TOKEN_TRELLO, HOSTENAME_, ID_LIST_TECH_NEW, ID_LIST_CREO_NEW, \
    ID_LIST_TECH_EGOR, ID_LIST_TECH_GLEB


class TrelloManager:

    def __init__(self):
        self.__url_card = "https://api.trello.com/1/cards/"
        self.__url_lebel = "https://api.trello.com/1/labels/"
        self.__url_list = "https://api.trello.com/1/lists/"
        self.__url_webhook = "https://api.trello.com/1/webhooks/"
        self.__default_body = {'key': API_KEY_TRELLO, 'token': TOKEN_TRELLO}

    # CREATE LABEL
    def _create_label(self, username, board_id):
        query = {'name': f'{username}', 'color': 'black', 'idBoard': board_id}
        response = requests.request("POST", url=self.__url_lebel, json=query | self.__default_body)
        return literal_eval(response.text)['id']

    # CREATE CARD
    def _create_card(self, card_name, card_desc, card_date, labels, list_id):
        query = {'idList': list_id, 'name': card_name, 'desc': card_desc, 'idLabels': labels, 'due': card_date}
        return requests.request(
            "POST",
            url=self.__url_card,
            headers={"Accept": "application/json", 'Content-Type': 'application/json; charset=utf-8'},
            json=query | self.__default_body
        )

    # CREATE WEBHOOK CARD
    def _set_webhook_card(self, card_id, name="webhook"):
        query = {'callbackURL': f'{HOSTENAME_}', 'idModel': card_id, 'description': f'{name}_card_{card_id}'}
        return requests.post(
            self.__url_webhook,
            headers={'Content-Type': 'application/json'},
            json=query | self.__default_body
        )

    def _get_cards(self, list_id):
        return requests.request(
            "GET",
            url=f"{self.__url_list}{list_id}/cards",
            headers={"Accept": "application/json"},
            params=self.__default_body
        )

    def _delete_card(self, id_card):
        return requests.request(
            "DELETE",
            url=self.__url_card + id_card,
            headers={"Accept": "application/json"},
            params=self.__default_body
        )

    def _write_comment(self, id_card, text):
        return requests.request(
            "POST",
            url=self.__url_card + id_card + "/actions/comments",
            headers={"Accept": "application/json"},
            json={'text': text} | self.__default_body
        )

