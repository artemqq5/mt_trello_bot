from data.DefaultMySQL import DefaultMySQL


class AffRepository(DefaultMySQL):

    def __init__(self):
        super().__init__()

    def add(self, description, id_user):
        command = "INSERT INTO `cards_aff` (`description`,`id_user`) VALUES (%s, %s)"
        return self._insert_id(command, (description, id_user))

    def card(self, id_):
        command = "SELECT * FROM `cards_aff` WHERE `id` = %s;"
        return self._select_one(command, (id_,))

    def update_id_url(self, card_id_trello, url_card, id_):
        command = "UPDATE `cards_aff` SET `id_card` = %s, `url` = %s WHERE `id` = %s;"
        return self._update(command, (card_id_trello, url_card, id_))

    def card_by_id(self, id_):
        command = "SELECT * FROM `cards_aff` WHERE `id_card` = %s;"
        return self._select_one(command, (id_,))

