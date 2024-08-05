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

    def update_lang(self, id_user, lang):
        query = "UPDATE `users` SET `lang` = %s WHERE `id_user` = %s;"
        return self._select_one(query, (lang, id_user))

    def update_username(self, id_user, username):
        query = "UPDATE `users` SET `username` = %s WHERE `id_user` = %s;"
        return self._select_one(query, (username, id_user))

    def update_firstname(self, id_user, firstname):
        query = "UPDATE `users` SET `firstname` = %s WHERE `id_user` = %s;"
        return self._select_one(query, (firstname, id_user))

    #####

    def designers(self):
        command = "SELECT * FROM `users` WHERE `dep_user` = 'designer';"
        return self._select_all(command)

    def admins(self):
        command = "SELECT * FROM `users` WHERE `dep_user` = 'admin';"
        return self._select_all(command)


