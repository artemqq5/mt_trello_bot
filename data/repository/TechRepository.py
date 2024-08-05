from data.DefaultMySQL import DefaultMySQL


class TechRepository(DefaultMySQL):

    def __init__(self):
        super().__init__()

    def add(self, name, date, id_user, tech):
        command = "INSERT INTO `cards_tech` (`name`, `date`, `id_user`, `tech`) VALUES (%s, %s, %s, %s)"
        return self._insert_id(command, (name, date, id_user, tech))

    def card(self, id_):
        command = "SELECT * FROM `cards_tech` WHERE `id` = %s;"
        return self._select_one(command, (id_,))

    def update_url_id(self, card_id_trello, url_card, id_):
        command = "UPDATE `cards_tech` SET `id_card` = %s, `url` = %s WHERE `id` = %s;"
        return self._update(command, (card_id_trello, url_card, id_))

    def card_by_id(self, id_):
        command = "SELECT * FROM `cards_tech` WHERE `id_card` = %s;"
        return self._select_one(command, (id_, ))
