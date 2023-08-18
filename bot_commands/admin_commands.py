from db_helper.db_manager import *
from bot_helper.menu_buttons import *
from messages.const_messages import *
from bot_commands.state_managment import *
import datetime
from telebot import types
from telebot.types import BotCommand
from db_helper.db_manager import get_user_db, get_list_users_db
from messages.const_messages import ERROR_OPERATION, NOT_ACCESS, NOT_REGISTERED_USER
from bot_helper.af_manager_buttons import *
from bot_helper.gambling_fb_buttons import *
from bot_helper.gambling_ppc_buttons import *
from bot_helper.gambling_uac_buttons import *
from bot_helper.masons_partners import masons_partners_menu
from bot_helper.media_buttons import *
from models.task_form import *
from private_config import local_telegram_token, server_telegram_token
from telebot.async_telebot import AsyncTeleBot
import asyncio
from trello_helper.trello_manager import *


async def get_all_command(message, bot):
    try:
        list_users = ""
        for user in get_list_users_db().result:
            list_users += f"{user['id_user']} | {user['name_user']} | {user['dep_user']}\n"
        await bot.send_message(message.chat.id, list_users, reply_markup=close_markup)
    except Exception as e:
        print(f"exception when get_all() : {e}")
        await bot.send_message(message.chat.id, ERROR_OPERATION, reply_markup=close_markup)


async def add_user_command(message, bot):
    list_data_user = message.text.split(" ")
    if len(list_data_user) == 3:
        if list_data_user[2] in dep_states:
            if get_user_db(list_data_user[0]).result is not None:
                await bot.send_message(message.chat.id, USER_ALREADY_HAVE, reply_markup=setStartButton())
            else:
                if add_user_db(User(
                        list_data_user[0],
                        list_data_user[1],
                        list_data_user[2],
                        create_label(list_data_user[1], "tech")["id"],
                        create_label(list_data_user[1], "creo")["id"])).result:
                    await bot.send_message(message.chat.id, USER_ADDED, reply_markup=setStartButton())
                else:
                    await bot.send_message(message.chat.id, USER_ADD_ERROR)
        else:
            await bot.reply_to(message, f'{HAVE_NOT_DEP} {tuple(dep_states)} :')
    else:
        await bot.reply_to(message, INPUT_USER_ADD_ERROR)


async def delete_user_command(message, bot):
    if get_user_db(message.text).result is not None:
        if delete_user_db(message.text).result:
            await bot.send_message(message.chat.id, USER_DELETED, reply_markup=setStartButton())
        else:
            await bot.send_message(message.chat.id, ERROR_DELETE_USER, reply_markup=setStartButton())
    else:
        await bot.reply_to(message, USER_HAVE_NOT_IN_DB)


async def mailing_all_command(message, bot):
    users = get_list_users_db()
    unsuccessful = 1
    user_error = ""

    for i in users.result:
        try:
            if i['id_user'] != str(message.chat.id):
                await bot.send_message(i['id_user'], message.text)
        except Exception as e:
            print(f"mailing all error for user {i}: {e}")
            unsuccessful += 1
            user_error += f"{i['name_user']}\n"

    await bot.reply_to(
        message,
        f"📬 Успішно доставлено {len(users.result) - unsuccessful} користувачам з {len(users.result)}\n\n"
        f"Досі не зареєструвалися у боті: \n{user_error}",
        reply_markup=setStartButton()
    )
