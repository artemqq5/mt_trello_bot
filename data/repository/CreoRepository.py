from data.DefaultMySQL import DefaultMySQL


class CreoRepository(DefaultMySQL):

    def __init__(self):
        super().__init__()

    def add(self, id_user, type, category, description, geo, language, currency, format, offer, voice,
            platform, source, deadline, count):
        command = "INSERT INTO `cards_creo` (`id_user`, `type`, `category`, `description`, `geo`, `language`, `currency`, `format`, `offer`, `voice`, `platform`, `source`, `deadline`, `count`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        return self._insert_id(command, (id_user, type, category, description, geo, language, currency,
                                         format, offer, voice, platform, source, deadline, count))

    def card(self, id_):
        command = "SELECT * FROM `cards_creo` WHERE `id` = %s;"
        return self._select_one(command, (id_,))

    def card_trello_id(self, id_):
        command = "SELECT * FROM `cards_creo` WHERE `id_card` = %s;"
        return self._select_one(command, (id_,))

    def update_id_url(self, card_id_trello, url_card, id_):
        command = "UPDATE `cards_creo` SET `id_card` = %s, `url` = %s WHERE `id` = %s;"
        return self._update(command, (card_id_trello, url_card, id_))

    def card_by_id(self, id_):
        command = "SELECT * FROM `cards_creo` WHERE `id_card` = %s;"
        return self._select_one(command, (id_,))