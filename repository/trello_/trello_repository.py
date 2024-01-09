from constants.base import CREO, TECH
from repository.trello_.trello_manager import TrelloManager


class TrelloRepository(TrelloManager):

    def __init__(self):
        super().__init__()

    def create_label_creo(self, name):
        return self._create_label(name, CREO)

    def create_label_tech(self, name):
        return self._create_label(name, TECH)

    def create_card_creo(self, card, labels):
        return self._create_card(card, labels, CREO)

    def create_card_tech(self, card, labels):
        return self._create_card(card, labels, TECH)

    def add_attachments_card(self, card_id, source):
        return self._add_attachments_card(card_id, source)

    def get_tasks_creo(self, user_label):
        return self._get_tasks(CREO, user_label)

    def get_tasks_tech(self, user_label):
        return self._get_tasks(TECH, user_label)

    def get_callback_cards(self):
        return self._get_callback_cards()

    def get_card(self, id_card):
        return self._get_card(id_card)

    def delete_card(self, id_card):
        return self._delete_card(id_card)

    def write_comment(self, id_card, text):
        return self._write_comment(id_card, text)

    def set_webhook(self, card_id):
        return self._set_webhook_card(card_id)
