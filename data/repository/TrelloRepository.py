from data.TrelloManager import TrelloManager
from data.repository.CreoRepository import CreoRepository
from data.repository.TechRepository import TechRepository
from private_config import ID_LIST_CREO_NEW, cards_label_trello, ID_LIST_TECH_GLEB, ID_LIST_TECH_EGOR


class TrelloRepository(TrelloManager):

    def create_creo_task(self, data, user, i18n):

        add_card_to_database = CreoRepository().add(
            id_user=user['id_user'], type=data['type'], category=data['category'], description=data['desc'],
            geo=data['geo'], language=data['lang'], currency=data['currency'], format=data['format'],
            offer=data['offer'], voice=data['voice'], source=data['source'], deadline=data.get('deadline', None),
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
            labels=[user['label_creo'], cards_label_trello[user['dep_user']]]
        )

        # try to load card to Trelo
        if not load_card_to_trello.content:
            print("ERROR(creo): try to load card to Trelo")
            return False

        json_card = load_card_to_trello.json()

        # set webhook to card
        if not self._set_webhook_card(json_card['id']):
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

        load_card_to_trello = TrelloManager()._create_card(
            card_name=i18n.TECH.CARD_NAME(id=add_card_to_database, category=data['category']),
            card_desc=i18n.TECH.CARD_DESC(desc=data['description_card'], username=user.get('username', " ")),
            card_date=data.get('deadline', None),
            list_id=ID_LIST_TECH_GLEB if data['tech'] == i18n.TECH.GLEB() else ID_LIST_TECH_EGOR,
            labels=[user['label_tech'], cards_label_trello[user['dep_user']]]
        )

        # try to load card to Trelo
        if not load_card_to_trello.content:
            print("ERROR(tech): try to load card to Trelo")
            return False

        json_card = load_card_to_trello.json()

        # set webhook to card
        if not self._set_webhook_card(json_card['id']):
            print("ERROR(tech): set webhook to card")

        # update database card`s id and url from trello
        if not TechRepository().update_id_url(json_card['id'], json_card['shortUrl'], add_card_to_database):
            print("ERROR(tech): update database card`s id and url from trello")

        return add_card_to_database
