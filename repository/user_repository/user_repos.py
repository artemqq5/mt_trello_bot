from repository.model.user import UserModel
from repository.my_connection import MyConnection


class UserRepository(MyConnection):
    def __init__(self):
        super().__init__()

    def add_user(self, user: UserModel):
        command = "INSERT INTO `users` (`id_user`, `name_user`, `dep_user`, `label_tech`, `label_creo`) VALUES (%s, %s, %s, %s, %s);"
        args = (user.id, user.name, user.dep, user.label_tech, user.label_creo)
        return self._insert(command, args)

    def delete_user(self, id_user):
        command = "DELETE FROM `users` WHERE `id_user` = %s;"
        args = (id_user,)
        return self._delete(command, args)

    def get_user(self, id_user):
        command = "SELECT * FROM `users` WHERE `id_user` = %s;"
        args = (id_user,)
        return self._select_one(command, args)

    def get_users(self):
        command = "SELECT * FROM `users`;"
        return self._select_all(command)

    def get_users_by_dep(self, dep):
        command = "SELECT * FROM `users` WHERE `dep_user` = %s;"
        args = (dep,)
        return self._select_all(command, args)
