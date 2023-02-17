import pymysql.cursors

from config import DEBUG_MODE
from private_config import local_password_connection, local_name_db, server_password_connection, server_name_db

# connection settings
if DEBUG_MODE:
    CONNECTION_PASSWORD = local_password_connection
    DB_NAME = local_name_db
else:
    CONNECTION_PASSWORD = server_password_connection
    # Нужно создать базу с таблицами на сервере !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
                add_user_command = "INSERT INTO `users_tb` VALUES ('{0}','{1}','{2}');" \
                    .format(user.id_user, user.name_user, user.dep_user)
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
                delete_user_command = f"DELETE FROM `users_tb` WHERE `id_user` = '{id_user}';"
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
                check_user_command = f"SELECT * FROM `users_tb` WHERE `id_user` = '{user_id}';"

                cursor.execute(check_user_command)
                result = cursor.fetchall()[0]

            connection.commit()
            return ResultData(
                User(result['id_user'], result['name_user'], result['dep_user']),
                "good"
            )
    except Exception as e:
        print(f"get_user: {e}")
        return ResultData(None, f"error: {e}")


def get_list_users():
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                check_user_command = f"SELECT * FROM `users_tb`;"

                cursor.execute(check_user_command)
                result = cursor.fetchall()

            connection.commit()
            return ResultData(result, "good")
    except Exception as e:
        print(f"get_user: {e}")
        return ResultData(None, f"error: {e}")


class User:
    def __init__(self, id_user, name_user, dep_user):
        self.name_user = name_user
        self.id_user = id_user
        self.dep_user = dep_user


class ResultData:
    def __init__(self, result, message):
        self.result = result
        self.message = message
