import requests

from data.TrelloManager import TrelloManager
from data.const import BUYERS_ROLE_LIST
from data.repository.AffRepository import AffRepository
from data.repository.CreoRepository import CreoRepository
from data.repository.TechRepository import TechRepository
from private_config import *


class TrelloRepository(TrelloManager):

    def create_creo_task(self, data, user, i18n):
        add_card_to_database = CreoRepository().add(
            id_user=user['id_user'], type=data['type'], category=data['category'], description=data['desc'],
            geo=data['geo'], language=data['lang'], currency=data['currency'], format=data['format'],
            offer=data['offer'], voice=data['voice'], platform=data['platform'], source=data['source'],
            deadline=data.get('deadline', None),
            count=data['count']
        )

        # Try to add card to local database
        if not add_card_to_database:
            print("ERROR(creo): Try to add card to local database")
            return False

        load_card_to_trello = TrelloManager()._create_card(
            card_name=i18n.CREO.CARD_NAME(id=add_card_to_database, type=data['type'], category=data['category']),
            card_desc=i18n.CREO.CARD_DESC(
                type=data['type'],
                category=data['category'],
                platform=data['platform'],
                geo=data['geo'],
                lang=data['lang'],
                currency=data['currency'],
                format=data['format'],
                offer=data['offer'],
                voice=data['voice'],
                source=data['source'],
                count=data['count'],
                username=user['username'],
                desc=data['desc'],
            ),
            card_date=data.get('deadline', None),
            list_id=ID_LIST_CREO_NEW,
            labels=[user['label_creo'], cards_label_trello_creo[user['dep_user']]]
        )

        # try to load card to Trelo
        if not load_card_to_trello or not load_card_to_trello.content:
            print("ERROR(creo): try to load card to Trelo")
            print(load_card_to_trello)
            return False

        try:
            json_card = load_card_to_trello.json()
        except requests.exceptions.JSONDecodeError:
            print("ERROR(creo): Failed to parse JSON from Trello response")
            print(f"Trello Response: {load_card_to_trello.text}")
            return False

        # set webhook to card
        if not self._set_webhook_card(json_card['id'], "creo"):
            print("ERROR(creo): set webhook to card")

        # update database card`s id and url from trello
        if not CreoRepository().update_id_url(json_card['id'], json_card['shortUrl'], add_card_to_database):
            print("ERROR(creo): update database card`s id and url from trello")

        return add_card_to_database

    def create_tech_task(self, data, user, i18n):

        add_card_to_database = TechRepository().add(
            category=data['category'], description=data['description_card'], deadline=data.get('deadline', None),
            id_user=user['id_user'], tech=data['tech']
        )

        # Try to add card to local database
        if not add_card_to_database:
            print("ERROR(tech): Try to add card to local database")
            return False

        if user['dep_user'] in BUYERS_ROLE_LIST:
            desc = i18n.TECH.CARD_DESC_TDS_ID(
                desc=data['description_card'],
                username=user.get('username', " "),
                tds_id=user.get('tds_buyer_id', '-'))
        else:
            desc = i18n.TECH.CARD_DESC(desc=data['description_card'], username=user.get('username', " "))

        load_card_to_trello = TrelloManager()._create_card(
            card_name=i18n.TECH.CARD_NAME(id=add_card_to_database, category=data['category']),
            card_desc=desc,
            card_date=data.get('deadline', None),
            list_id=ID_LIST_TECH_GLEB if data['tech'] == "Gleb" else ID_LIST_TECH_EGOR,
            labels=[user['label_tech'], cards_label_trello_tech[user['dep_user']]]
        )

        # try to load card to Trelo
        if not load_card_to_trello or not load_card_to_trello.content:
            print("ERROR(tech): Failed to create card in Trello")
            print(load_card_to_trello)
            return False

        try:
            json_card = load_card_to_trello.json()
        except requests.exceptions.JSONDecodeError:
            print("ERROR(tech): Failed to parse JSON from Trello response")
            print(f"Trello Response: {load_card_to_trello.text}")
            return False

        # set webhook to card
        if not self._set_webhook_card(json_card['id'], "tech"):
            print("ERROR(tech): set webhook to card")

        # update database card`s id and url from trello
        if not TechRepository().update_id_url(json_card['id'], json_card['shortUrl'], add_card_to_database):
            print("ERROR(tech): update database card`s id and url from trello")

        return add_card_to_database

    @staticmethod
    def create_aff_task(data, user, i18n):

        add_card_to_database = AffRepository().add(
            description=data['desc'], id_user=user['id_user']
        )

        # Try to add card to local database
        if not add_card_to_database:
            print("ERROR(aff): Try to add card to local database")
            return False

        load_card_to_trello = TrelloManager()._create_card(
            card_name=i18n.AFF.CARD_NAME(id=add_card_to_database),
            card_desc=i18n.AFF.CARD_DESC(desc=data['desc'], username=user.get('username', " ")),
            card_date=None,
            list_id=ID_LIST_AFFILIATE_NEW,
            labels=None
        )

        # try to load card to Trelo
        if not load_card_to_trello or not load_card_to_trello.content:
            print("ERROR(aff): try to load card to Trelo")
            print(load_card_to_trello)
            return False

        try:
            json_card = load_card_to_trello.json()
        except requests.exceptions.JSONDecodeError:
            print("ERROR(aff): Failed to parse JSON from Trello response")
            print(f"Trello Response: {load_card_to_trello.text}")
            return False

        # update database card`s id and url from trello
        if not AffRepository().update_id_url(json_card['id'], json_card['shortUrl'], add_card_to_database):
            print("ERROR(aff): update database card`s id and url from trello")

        return add_card_to_database

    def get_all_cards_by_user(self, id_user, i18n):
        all_cards = self._get_cards(ID_LIST_TECH_EGOR).json() + \
                    self._get_cards(ID_LIST_TECH_GLEB).json() + \
                    self._get_cards(ID_LIST_TECH_IN_PROCESS).json() + \
                    self._get_cards(ID_LIST_CREO_NEW).json()

        tech_cards_db = {card['id']: TechRepository().card_trello_id(card['id']) for card in all_cards}
        creo_cards_db = {card['id']: CreoRepository().card_trello_id(card['id']) for card in all_cards}

        cards_list = []

        for card in all_cards:
            card_id = card['id']
            card_db = tech_cards_db.get(card_id) or creo_cards_db.get(card_id)

            if card_db and card_db['id_user'] == str(id_user):
                list_card = dict(card_db)
                list_card["emoji"] = i18n.MY_TASK.TECH_EMOJI() if tech_cards_db.get(
                    card_id) else i18n.MY_TASK.CREO_EMOJI()
                cards_list.append(list_card)

        return sorted(cards_list, key=lambda card: card['date'], reverse=True)
