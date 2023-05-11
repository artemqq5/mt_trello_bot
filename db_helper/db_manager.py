import pymysql.cursors

from config import DEBUG_MODE
from private_config import local_password_connection, local_name_db, server_password_connection, server_name_db

# connection settings
if DEBUG_MODE:
    CONNECTION_PASSWORD = local_password_connection
    DB_NAME = local_name_db
else:
    CONNECTION_PASSWORD = server_password_connection
    DB_NAME = server_name_db


# make db connection
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password=CONNECTION_PASSWORD,
        db=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


# add user to db
def add_user(user):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                add_user_command = "INSERT INTO `users` VALUES ('{0}','{1}','{2}', '{3}', '{4}');" \
                    .format(user.id_user, user.name_user, user.dep_user, user.label_tech, user.label_creo)
                cursor.execute(add_user_command)

            connection.commit()
            return ResultData(True, "good")
    except Exception as e:
        print(f"add_user: {e}")
        return ResultData(False, e)


# delete user from tb
def delete_user(id_user):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                delete_user_command = f"DELETE FROM `users` WHERE `id_user` = '{id_user}';"
                cursor.execute(delete_user_command)

            connection.commit()
            return ResultData(True, "good")
    except Exception as e:
        print(f"delete_user: {e}")
        return ResultData(False, e)


# return a user by his chat.id
def get_user(user_id):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                check_user_command = f"SELECT * FROM `users` WHERE `id_user` = '{user_id}';"

                cursor.execute(check_user_command)
                result = cursor.fetchall()[0]

            connection.commit()
            return ResultData(
                User(
                    result['id_user'],
                    result['name_user'],
                    result['dep_user'],
                    result['label_tech'],
                    result['label_creo'],
                ),
                "good"
            )
    except Exception as e:
        print(f"get_user: {e}")
        return ResultData(None, f"error: {e}")


def get_list_users():
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                check_user_command = f"SELECT * FROM `users`;"

                cursor.execute(check_user_command)
                result = cursor.fetchall()

            connection.commit()
            return ResultData(result, "good")
    except Exception as e:
        print(f"get_list_users: {e}")
        return ResultData(None, f"error: {e}")


def add_card(name, desc, tb_name, id_user, id_card='null'):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                card_add_command = f"INSERT INTO `{tb_name}` (`name`, `desc`, `id_user`, `id_card`) VALUES ('{name}', '{desc}', '{id_user}', '{id_card}');"
                get_num_last_card = f"SELECT `id` FROM `{tb_name}`;"

                cursor.execute(card_add_command)
                cursor.execute(get_num_last_card)
                result = cursor.fetchall()

            connection.commit()
            return ResultData(result[len(result)-1], "good")
    except Exception as e:
        print(f"add_card: {e}")
        return ResultData(None, f"error: {e}")


def update_card(id_pk, id_card, tb_name):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                card_update_command = f"UPDATE `{tb_name}` SET `id_card` = '{id_card}' WHERE `id` = '{id_pk}';"
                cursor.execute(card_update_command)

            connection.commit()
    except Exception as e:
        print(f"update_card: {e}")


class User:
    def __init__(self, id_user, name_user, dep_user, label_tech, label_creo):
        self.name_user = name_user
        self.id_user = id_user
        self.dep_user = dep_user
        self.label_tech = label_tech
        self.label_creo = label_creo


class ResultData:
    def __init__(self, result, message):
        self.result = result
        self.message = message
