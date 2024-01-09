from repository.model.card_creo import CardModelCreo
from repository.model.card_tech import CardModelTech
from repository.my_connection import MyConnection


class CardRepository(MyConnection):
    def __init__(self):
        super().__init__()

    def add_card_creo(self, card: CardModelCreo):
        command = """
        INSERT INTO `cards_creo` (
            `name`, `date`, `id_user`, `format`, `type`, `category`, `description`, `geo`, `language`, `currency`, `format_res`, `offer`, `voice`, `source`, `deadline`, `sub_desc`, `count`
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
        args = (
            card.name, card.date, card.id_user, card.format_, card.type_, card.category,
            card.description, card.geo, card.language, card.currency, card.format_res, card.offer,
            card.voice, card.source, card.deadline, card.sub_desc, card.count
        )
        return self._insert_id(command, args)

    def get_card_creo(self, id_):
        command = "SELECT * FROM `cards_creo` WHERE `id` = %s;"
        args = (id_,)
        return self._select_one(command, args)

    def update_card_creo(self, card_id_trello, url_card, id_):
        command = "UPDATE `cards_creo` SET `id_card` = %s, `url` = %s WHERE `id` = %s;"
        args = (card_id_trello, url_card, id_)
        return self._update(command, args)

    def add_card_tech(self, card: CardModelTech):
        command = "INSERT INTO `cards_tech` (`name`, `date`, `id_user`) VALUES (%s, %s, %s)"
        args = (card.name, card.date, card.id_user)
        return self._insert_id(command, args)

    def get_card_tech(self, id_):
        command = "SELECT * FROM `cards_tech` WHERE `id` = %s;"
        args = (id_,)
        return self._select_one(command, args)

    def update_card_tech(self, card_id_trello, url_card, id_):
        command = "UPDATE `cards_tech` SET `id_card` = %s, `url` = %s WHERE `id` = %s;"
        args = (card_id_trello, url_card, id_)
        return self._update(command, args)
