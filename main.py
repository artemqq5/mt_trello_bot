from config import DEBUG_MODE
from db_manager import add_user, User, delete_user, get_user, get_list_users
from menu_buttons import setStartButton
from private_config import local_telegram_token, server_telegram_token
from trello_manager import create_card
from telebot.async_telebot import AsyncTeleBot
import asyncio
import threading

# bot settings
if DEBUG_MODE:
    bot = AsyncTeleBot(local_telegram_token)
else:
    bot = AsyncTeleBot(server_telegram_token)

# states
modes = {"none", "add_user", "delete_user", "mailing_all"}
user_state = "none"

# dep states
dep_states = {"admin", "gamble_ppc", "gamble_uac", "gamble_fb", "af_manager", "the_PR"}


# set operations state 'none'
def set_state_none():
    global user_state
    user_state = "none"


# send start text for user COMMAND
@bot.message_handler(commands=['start'])
async def start_message(message):
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        await bot.send_message(message.chat.id, 'Меню', reply_markup=setStartButton())
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


# management user (add, delete)
@bot.message_handler(commands=['add_user', 'delete_user', 'mailing_all'])
async def menu_(message):
    global user_state
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        if get_user(message.chat.id).result.dep_user == "admin":
            if message.text == '/add_user':
                user_state = "add_user"
                await bot.send_message(message.chat.id, 'Введите пользователя формат id name dep : ')
            elif message.text == '/delete_user':
                user_state = "delete_user"
                await bot.send_message(message.chat.id, 'Введите id пользователя : ')
            elif message.text == '/mailing_all':
                user_state = "mailing_all"
                await bot.send_message(message.chat.id, 'Введите сообщение для рассылки всем пользователям : ')
        else:
            await bot.send_message(message.chat.id, 'У вас нет доступа, напишите админу')
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


@bot.message_handler(func=lambda m: user_state in ("add_user", "delete_user"))
async def user_delete_add(message):
    if user_state == "add_user":
        listDataUser = message.text.split(" ")
        if len(listDataUser) == 3:
            if get_user(listDataUser[0]).result is not None:
                set_state_none()  # reset user state
                await bot.reply_to(message, 'Пользователь уже в базе')
            else:
                if add_user(User(listDataUser[0], listDataUser[1], listDataUser[2])).result:
                    set_state_none()  # reset user state
                    await bot.reply_to(message, 'Пользователь добавлен')
                else:
                    await bot.reply_to(message, 'Ошибка ввода. Используйте формат id name dep :')
        else:
            await bot.reply_to(message, 'Ошибка ввода. Используйте формат id name dep :')
    elif user_state == "delete_user":
        if get_user(message.text).result is not None:
            set_state_none()  # reset user state

            if delete_user(message.text).result:
                await bot.reply_to(message, 'Пользователь успешно удален')
            else:
                await bot.reply_to(message, 'Не вышло удалить пользователя, напишите админу')
        else:
            await bot.reply_to(message, 'Такого пользователя нет в базе, повторите попытку :')


@bot.message_handler(func=lambda m: user_state == "mailing_all")
async def user_delete_add(message):
    set_state_none()  # reset user state

    users = get_list_users()
    unsuccessful = 0

    for i in users.result:
        try:
            if i['id_user'] != str(message.chat.id):
                await bot.send_message(i['id_user'], message.text)
            else:
                unsuccessful += 1
        except Exception as e:
            print(f"mailing all error for user {i}")
            unsuccessful += 1

    await bot.reply_to(
        message,
        f"Успешно доставлено {len(users.result) - unsuccessful} пользователям из {len(users.result)}"
    )


# create card, other text
# @bot.message_handler(func=lambda message: True)
# async def echo_all(message):
#     if check_auth(message.chat.id).result:
#         match user_state["operation"]:
#             case 0:  # none
#                 await bot.reply_to(message, "Бот не понимает команду")
#             case 1:  # create_card
#                 set_state_none()  # set operations state 'none'
#                 t1 = threading.Thread(target=create_card, args=(message.text,))
#                 t1.start()
#                 t1.join()
#                 await bot.reply_to(message, "Карточка '{0}' успешно создана".format(message.text))
#             case _:
#                 set_state_none()  # set operations state 'none'
#                 await bot.reply_to(message, "error input")
#     else:
#         set_state_none()  # set operations state 'none'
#         await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
