from config import DEBUG_MODE
from db_manager import check_auth, add_user, User, delete_user, get_user
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
modes = {"none": 0, "create_card": 1, "add_user": 2, "delete_user": 3}
user_state = {"operation": modes["none"]}

# dep states
dep_states = {"admin": 1, }


# set operations state 'none'
def user_state_none():
    user_state["operation"] = modes["none"]


# send start text for user COMMAND
@bot.message_handler(commands=['start'])
async def start_message(message):
    user_state_none()  # set operations state 'none'
    if check_auth(message.chat.id).result:
        await bot.send_message(message.chat.id, 'Меню', reply_markup=setStartButton())
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


# create card with your name COMMAND
# @bot.message_handler(commands=['create'])
# async def create_message(message):
#     if check_auth(message.chat.id).result:
#         user_state["operation"] = modes["create_card"]
#         await bot.send_message(message.chat.id, 'Введите название карточки:')
#     else:
#         user_state_none()  # set operations state 'none'
#         await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


# management user (add, delete)
@bot.message_handler(
    func=lambda message: message.text in ["Добавить пользователя ➕", "Удалить пользователя ➖"] or user_state[
        "operation"] in (modes["add_user"], modes["delete_user"]))
async def menu_operations(message):
    if check_auth(message.chat.id).result:
        if get_user(message.chat.id)['dep_user'] == dep_states['admin']:
            match message.text:
                case "Добавить пользователя ➕":
                    user_state["operation"] = modes["add_user"]
                    await bot.send_message(message.chat.id, 'Введите пользователя в формате id name dep :')
                case "Удалить пользователя ➖":
                    user_state["operation"] = modes["delete_user"]
                    await bot.send_message(message.chat.id,
                                           'Введите telegram ID пользователя, которого хотите удалить:')
                case _:
                    if user_state["operation"] == modes["add_user"]:
                        try:
                            listDataUser = message.text.split(" ")
                            if len(listDataUser) == 3:
                                if check_auth(listDataUser[0]).result:
                                    user_state_none()  # set operations state 'none'
                                    await bot.reply_to(message, 'Пользователь уже в базе')
                                else:
                                    if add_user(User(listDataUser[0], listDataUser[1], listDataUser[2])).result:
                                        user_state_none()  # set operations state 'none'
                                        await bot.reply_to(message, 'Пользователь добавлен')
                                    else:
                                        await bot.reply_to(message, 'Ошибка ввода. Используйте формат id name dep :')
                            else:
                                await bot.reply_to(message, 'Ошибка ввода. Используйте формат id name dep :')
                        except Exception as e:
                            print(f"parse data to create user error: {e}")
                    elif user_state["operation"] == modes["delete_user"]:
                        try:
                            idUser = message.text
                            if check_auth(idUser).result:

                                if delete_user(idUser).result:
                                    await bot.reply_to(message, 'Пользователь успешно удален')
                                else:
                                    await bot.reply_to(message, 'Не вышло удалить пользователя')

                                user_state_none()  # set operations state 'none'
                            else:
                                await bot.reply_to(message, 'Такого пользователя нет в базе, повторите попытку:')
                        except Exception as e:
                            print(f"parse data to delete user error: {e}")
                    else:
                        user_state_none()  # set operations state 'none'
                        await bot.reply_to(message, "Бот не понимает команду")
        else:
            user_state_none()  # set operations state 'none'
            await bot.send_message(message.chat.id, "У вас нет прав на выполнение данной команды")
    else:
        user_state_none()  # set operations state 'none'
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


# create card, other text
@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    if check_auth(message.chat.id).result:
        match user_state["operation"]:
            case 0:  # none
                await bot.reply_to(message, "Бот не понимает команду")
            case 1:  # create_card
                user_state_none()  # set operations state 'none'
                t1 = threading.Thread(target=create_card, args=(message.text,))
                t1.start()
                t1.join()
                await bot.reply_to(message, "Карточка '{0}' успешно создана".format(message.text))
            case _:
                user_state_none()  # set operations state 'none'
                await bot.reply_to(message, "error input")
    else:
        user_state_none()  # set operations state 'none'
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу')


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
