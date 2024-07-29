from data.DefaultMySQL import DefaultMySQL


class UserRepository(DefaultMySQL):

    def __init__(self):
        super().__init__()

    def add(self, id_user, name_user, dep_user, label_tech, label_creo):
        command = "INSERT INTO `users` (`id_user`, `name_user`, `dep_user`, `label_tech`, `label_creo`) VALUES (%s, %s, %s, %s, %s);"
        return self._insert(command, (id_user, name_user, dep_user, label_tech, label_creo))

    def delete(self, id_user):
        command = "DELETE FROM `users` WHERE `id_user` = %s;"
        return self._delete(command, (id_user,))

    def user(self, id_user):
        command = "SELECT * FROM `users` WHERE `id_user` = %s;"
        return self._select_one(command, (id_user,))

    def users(self):
        command = "SELECT * FROM `users`;"
        return self._select_all(command)

    def users_by_dep(self, dep):
        command = "SELECT * FROM `users` WHERE `dep_user` = %s;"
        return self._select_all(command, (dep,))

    def update_lang(self, user_id, lang):
        query = "UPDATE `users` SET `lang` = %s WHERE `user_id` = %s;"
        return self._select_one(query, (lang, user_id))
