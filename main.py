import datetime
from telebot import types
from telebot.types import BotCommand

from bot_helper.af_manager_buttons import *
from bot_helper.gambling_fb_buttons import *
from bot_helper.gambling_ppc_buttons import *
from bot_helper.gambling_uac_buttons import *
from bot_helper.media_buttons import *
from db_helper.db_manager import *
from bot_helper.menu_buttons import *
from messages.const_messages import *
from models.task_form import *
from private_config import local_telegram_token, server_telegram_token
from telebot.async_telebot import AsyncTeleBot
import asyncio

from trello_helper.trello_manager import *

# bot settings
if DEBUG_MODE:
    bot = AsyncTeleBot(local_telegram_token)
else:
    bot = AsyncTeleBot(server_telegram_token)

# states
modes = {
    "none",
    "add_user",
    "delete_user",
    "mailing_all",

    "add_offer",
    "edit_offer",

    "order_creative",
    "order_creative_gamble",
    "share_app",
    "pwa_app",
    "create_campaign",

    "add_comment",

    "set_domain",
    "setting_cloak",
    "prepare_vait",
}

user_state = "none"

# dep states
dep_states = {"admin", "gambleppc", "gambleuac", "gamblefb", "afmngr", "media"}

# close markup
close_markup = types.ReplyKeyboardRemove(selective=False)


# set operations state 'none'
def set_state_none():
    global user_state
    user_state = "none"


# send start text for user COMMAND
@bot.message_handler(commands=['start'])
async def start_message(message):
    set_state_none()  # reset user state

    # await bot.set_my_commands(
    #     commands=[
    #         BotCommand("/start", "Меню"),
    #         BotCommand("/add_user", "Додати користувача"),
    #         BotCommand("/delete_user", "Видалити користувача"),
    #         BotCommand("/mailing_all", "Розсилка всім"),
    #         BotCommand("/get_all", "Показати всіх користувачів")])

    if get_user(message.chat.id).result is not None:
        await bot.send_message(message.chat.id, 'Меню', reply_markup=setStartButton())
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


# management user (add, delete)
@bot.message_handler(commands=['add_user', 'delete_user', 'mailing_all'])
async def menu_(message):
    global user_state
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        if get_user(message.chat.id).result.dep_user == "admin":
            if message.text == '/add_user':
                user_state = "add_user"
                await bot.send_message(
                    message.chat.id,
                    INPUT_USER_ADD,
                    reply_markup=close_markup
                )
            elif message.text == '/delete_user':
                user_state = "delete_user"
                await bot.send_message(message.chat.id, INPUT_USER_ID, reply_markup=close_markup)
            elif message.text == '/mailing_all':
                user_state = "mailing_all"
                await bot.send_message(
                    message.chat.id,
                    MAIL_TO_ALL,
                    reply_markup=close_markup
                )
        else:
            await bot.send_message(message.chat.id, NOT_ACCESS, reply_markup=close_markup)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(commands=['get_all'])
async def show_all(message):
    global user_state
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        if get_user(message.chat.id).result.dep_user == "admin":
            try:
                result = get_list_users()
                listUsers = ""
                for user in result.result:
                    listUsers += f"{user['id_user']} | {user['name_user']} | {user['dep_user']}\n"
                await bot.send_message(
                    message.chat.id,
                    listUsers,
                    reply_markup=close_markup)
            except Exception as e:
                print(e)
                await bot.send_message(message.chat.id, ERROR_OPERATION, reply_markup=close_markup)
        else:
            await bot.send_message(message.chat.id, NOT_ACCESS, reply_markup=close_markup)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state in ("add_user", "delete_user"))
async def user_delete_add(message):
    if get_user(message.chat.id).result is not None:
        if user_state == "add_user":
            listDataUser = message.text.split(" ")
            if len(listDataUser) == 3:
                if listDataUser[2] in dep_states:
                    if get_user(listDataUser[0]).result is not None:
                        set_state_none()  # reset user state
                        await bot.reply_to(message, USER_ALREADY_HAVE, reply_markup=setStartButton())
                    else:
                        if add_user(User(
                                listDataUser[0],
                                listDataUser[1],
                                listDataUser[2],
                                create_label(listDataUser[1], "tech")["id"],
                                create_label(listDataUser[1], "creo")["id"])).result:
                            set_state_none()  # reset user state
                            await bot.reply_to(message, USER_ADDED, reply_markup=setStartButton())
                        else:
                            await bot.reply_to(message, '')
                else:
                    await bot.reply_to(message, f'{HAVE_NOT_DEP} {tuple(dep_states)} :')
            else:
                await bot.reply_to(message, INPUT_USER_ADD_ERROR)
        elif user_state == "delete_user":
            if get_user(message.text).result is not None:
                set_state_none()  # reset user state

                if delete_user(message.text).result:
                    await bot.reply_to(message, USER_DELETED, reply_markup=setStartButton())
                else:
                    await bot.reply_to(
                        message,
                        ERROR_DELETE_USER,
                        reply_markup=setStartButton()
                    )
            else:
                await bot.reply_to(message, USER_HAVE_NOT_IN_DB)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "mailing_all")
async def user_mailing(message):
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        users = get_list_users()
        unsuccessful = 0

        for i in users.result:
            try:
                if i['id_user'] != str(message.chat.id):
                    await bot.send_message(i['id_user'], message.text)
                else:
                    unsuccessful += 1
            except Exception as e:
                print(f"mailing all error for user {i}: {e}")
                unsuccessful += 1

        await bot.reply_to(
            message,
            f"📬 Успішно доставлено {len(users.result) - unsuccessful} користувачам з {len(users.result)}",
            reply_markup=setStartButton()
        )
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(
    func=lambda m: m.text in ("Gambling FB", "Gambling PPC", "Gambling UAC", "AF Manager", "Media", "Мої Завдання 📋"))
async def choice_category(message):
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        match message.text:
            case "AF Manager":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=af_manager_menu())
            case "Media":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=media_menu())
            case "Gambling FB":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=gambling_fb_menu())
            case "Gambling PPC":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=gambling_ppc_menu())
            case "Gambling UAC":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=gambling_uac_menu())
            case "Мої Завдання 📋":
                await bot.send_message(message.chat.id, message.text + " : ", reply_markup=my_tasks_menu())
            case _:
                await bot.reply_to(message, "(У розробці)")
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "add_offer")
async def offer_add(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match task_step["step"]:
                case 0:
                    match message.text:
                        case "Новий":
                            model_task_list["type"] = "Новий"
                            model_task_list["operation"] = "Додати новий оффер"
                            set_task_step(1)
                            await bot.send_message(message.chat.id, "Група в тг :", reply_markup=close_markup)
                        case "Існуючий":
                            model_task_list["type"] = "Існуючий"
                            model_task_list["operation"] = "Додати існуючий оффер"
                            set_task_step(2)
                            await bot.send_message(message.chat.id, "Ім'я рекламодавця :", reply_markup=close_markup)
                        case _:
                            await bot.reply_to(message, "Виберіть із (Новий або Існуючий)")
                case 1:
                    model_task_list["tg_group"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Ім'я рекламодавця :")
                case 2:
                    model_task_list["adv_name"] = message.text
                    set_task_step(3)
                    await bot.send_message(message.chat.id, "Назва офферу :")
                case 3:
                    model_task_list["offer_name"] = message.text
                    set_task_step(4)
                    await bot.send_message(message.chat.id, "Гео :")
                case 4:
                    model_task_list["geo"] = message.text
                    set_task_step(5)
                    await bot.send_message(message.chat.id, "Відрахування з гео :")
                case 5:
                    model_task_list["reward_geo"] = message.text
                    set_task_step(6)
                    await bot.send_message(message.chat.id, "Промо посилання :")
                case 6:
                    set_state_none()  # reset user state
                    model_task_list["promo_link"] = message.text

                    if model_task_list["type"] == "Існуючий":
                        tg_group = ""
                    else:
                        tg_group = f"Група в тг: {model_task_list['tg_group']}\n"

                    desc_card = f"Тип: {model_task_list['type']}\n" \
                                f"{tg_group}" \
                                f"Ім'я рекламодавця: {model_task_list['adv_name']}\n" \
                                f"Назва офферу: {model_task_list['offer_name']}\n" \
                                f"Гео: {model_task_list['geo']}\n" \
                                f"Відрахування з гео: {model_task_list['reward_geo']}\n" \
                                f"Промо посилання: {model_task_list['promo_link']}\n" \
                                f"Зв'язок у тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Add offer by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} {model_task_list['operation']} ({model_task_list['offer_name']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )

                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND, reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "edit_offer")
async def offer_edit(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match task_step["step"]:
                case 0:
                    model_task_list["operation"] = "Редагувати оффер"
                    model_task_list["offer_id"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введіть опис, що зробити : ")
                case 1:
                    set_state_none()  # reset user state

                    model_task_list["desc_offer"] = message.text

                    desc_card = f"Id оффера у трекері : {model_task_list['offer_id']}\n" \
                                f"Задача : {model_task_list['desc_offer']}\n\n" \
                                f"Зв'язок у тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Edit offer by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} {model_task_list['operation']} ({model_task_list['offer_id']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )

                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND, reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "order_creative")
async def order_creo(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] in (4, 8):
            match task_step["step"]:
                case 0:
                    model_task_list["currency_type"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введіть гео : ")
                case 1:
                    model_task_list["geo"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Введіть таймінг відео (у секундах) : ")
                case 2:
                    model_task_list["timing_video"] = message.text
                    set_task_step(3)
                    await bot.send_message(
                        message.chat.id,
                        "Формат креативу: розмір (наприклад, 1000х1000 пікселів) ,"
                        " формат файлу (наприклад, mp4), необхідний розмір файлу (наприклад до 10 мб):"
                    )
                case 3:
                    model_task_list["format"] = message.text
                    set_task_step(4)
                    await bot.send_message(
                        message.chat.id,
                        "Вкладення для ТЗ: посилання на картинки/відео через кому"
                        "Наприклад: \nhttps://google.com/,https://google.com/"
                    )
                case 4:
                    try:
                        model_task_list["source"] = message.text.split(",")
                        set_task_step(5)
                        await bot.send_message(message.chat.id, "Введіть кількість креативів : ")
                    except Exception as e:
                        print(e)
                        await bot.send_message(message.chat.id, "Спробуйте ще раз (формат через кому) : ")
                case 5:
                    model_task_list["count"] = message.text
                    set_task_step(6)
                    await bot.send_message(message.chat.id, "Введіть оффер : ")
                case 6:
                    model_task_list["offer"] = message.text
                    set_task_step(7)
                    await bot.send_message(message.chat.id, "Введіть опис : ")
                case 7:
                    model_task_list["desc"] = message.text
                    set_task_step(8)
                    await bot.send_message(message.chat.id, "Введіть коротку назву картки : ")
                case 8:
                    if len(message.text) <= 40:
                        model_task_list["title"] = message.text
                        set_task_step(9)
                        await bot.send_message(
                            message.chat.id,
                            TIME_CHOICE,
                            reply_markup=choice_date()
                        )
                    else:
                        await bot.reply_to(message, "Коротка назва має бути до 40 символів : ")
                case 9:
                    try:
                        if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == SKIP:
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                        desc_card = f"Валюта : {model_task_list['currency_type']}\n" \
                                    f"Гео : {model_task_list['geo']}\n" \
                                    f"Таймінг відео : {model_task_list['timing_video']}\n" \
                                    f"Формат креативу : {model_task_list['format']}\n" \
                                    f"Кількість креативів : {model_task_list['count']}\n" \
                                    f"Оффер : {model_task_list['offer']}\n\n" \
                                    f"Опис додатково : \n{model_task_list['desc']}\n\n" \
                                    f"Зв'язок у тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"Order Creative by ({current_user.result.name_user})",
                            f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                            "cards_creo",
                            message.chat.id,
                        ).result

                        if result_add_to_db is not None:
                            card = card_id = create_card_creo(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} Креатив ({model_task_list['title']})",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_creo,
                                date=dateTime
                            )

                            update_card(result_add_to_db['id'], card.json()['id'], "cards_creo")

                            add_attachments_to_card(
                                card_id=card_id.json()['id'],
                                source=model_task_list['source']
                            )

                            if card_id.ok:
                                await bot.send_message(
                                    message.chat.id,
                                    MESSAGE_SEND,
                                    reply_markup=setStartButton()
                                )
                            else:
                                await bot.send_message(
                                    message.chat.id,
                                    MESSAGE_DONT_SEND,
                                    reply_markup=setStartButton()
                                )

                            set_state_none()  # reset user state
                        else:
                            await bot.send_message(
                                message.chat.id,
                                MESSAGE_DONT_SEND,
                                reply_markup=setStartButton()
                            )
                            set_state_none()  # reset user state

                    except Exception as e:
                        print(e)
                        if str(e).__contains__("does not match format '%Y-%m-%d %H:%M %z'"):
                            await bot.reply_to(
                                message,
                                WRONG_TIME_CHOICE
                            )
                        else:
                            set_state_none()  # reset user state
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "order_creative_gamble")
async def order_creo_gamble(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] in (3, 4, 12, 13, 14):
            match task_step["step"]:
                case 0:
                    try:
                        model_task_list["count"] = int(message.text)
                        set_task_step(1)
                        await bot.send_message(message.chat.id, "Введіть гео : ")
                    except Exception as e:
                        print(f"order gambling creo (input count of creo) {e}")
                        await bot.send_message(message.chat.id, "Введіть число : ")
                case 1:
                    model_task_list["geo"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Мова, валюта: (наприклад: CAD/або символ валюти) : ")
                case 2:
                    model_task_list["valuta"] = message.text
                    set_task_step(3)
                    await bot.send_message(
                        message.chat.id,
                        "Формат креативу: розмір (наприклад 1000х1000 пікселів),"
                        " формат файлу (наприклад, mp4), необхідний розмір файлу (наприклад до 10 мб):"
                    )
                case 3:
                    model_task_list["format"] = message.text
                    set_task_step(4)
                    await bot.send_message(
                        message.chat.id,
                        "Введіть оффер (бонуси, текст тощо): ",
                        reply_markup=skip_desc()
                    )
                case 4:
                    if message.text == SKIP:
                        model_task_list["offer"] = "Встанови та виграй"
                    else:
                        model_task_list["offer"] = message.text
                    set_task_step(5)
                    await bot.send_message(
                        message.chat.id,
                        "Назва слота або тематики (Book of RA або, наприклад, Ліприкон) : ",
                        reply_markup=close_markup
                    )
                case 5:
                    model_task_list["theme_name"] = message.text
                    set_task_step(6)
                    await bot.send_message(message.chat.id, "Емоції (Так, Ні) : ", reply_markup=yes_no())
                case 6:
                    if message.text == "Так":
                        model_task_list["emotions"] = "Так"
                    else:
                        model_task_list["emotions"] = "Ні"
                    set_task_step(7)
                    await bot.send_message(
                        message.chat.id,
                        "Плашки (Google, Apple, Google та Apple) : ",
                        reply_markup=plash_google_apple()
                    )
                case 7:
                    model_task_list["tabs"] = message.text
                    set_task_step(8)
                    await bot.send_message(message.chat.id, "SMS (Так, Ні) : ", reply_markup=yes_no())
                case 8:
                    if message.text == "Так":
                        model_task_list["sms"] = "Так"
                    else:
                        model_task_list["sms"] = "Ні"
                    set_task_step(9)
                    await bot.send_message(
                        message.chat.id,
                        "Телефон із повідомленням (Так, Ні) : ",
                        reply_markup=yes_no()
                    )
                case 9:
                    if message.text == "Так":
                        model_task_list["phone_notify"] = "Так"
                    else:
                        model_task_list["phone_notify"] = "Ні"
                    set_task_step(10)
                    await bot.send_message(
                        message.chat.id,
                        "Назва банку (якщо потрібний конкретний) : ",
                        reply_markup=skip_desc()
                    )
                case 10:
                    if message.text == SKIP:
                        model_task_list["name_bank"] = "-"
                    else:
                        model_task_list["name_bank"] = message.text
                    set_task_step(11)
                    await bot.send_message(message.chat.id, "Озвучка (якщо треба) : ", reply_markup=skip_desc())
                case 11:
                    if message.text == SKIP:
                        model_task_list["sound"] = "-"
                    else:
                        model_task_list["sound"] = message.text
                    set_task_step(12)
                    await bot.send_message(message.chat.id, "Опис (нюанси, побажання) : ", reply_markup=skip_desc())
                case 12:
                    if message.text == SKIP:
                        model_task_list["desc"] = "відсутній"
                    else:
                        model_task_list["desc"] = message.text
                    set_task_step(13)
                    await bot.send_message(
                        message.chat.id,
                        "Вкладення для ТЗ: посилання на картинки/відео через кому"
                        "Наприклад: \nhttps://google.com/,https://google.com/",
                        reply_markup=close_markup
                    )
                case 13:
                    try:
                        model_task_list["reference"] = message.text.split(",")
                        if model_task_list["count"] > 1:
                            set_task_step(14)
                            await bot.send_message(
                                message.chat.id,
                                "Напишіть чим повинні відрізнятись інші крео (або заповніть форму під інші!) : ",
                                reply_markup=skip_desc()
                            )
                        else:
                            set_task_step(15)
                            await bot.send_message(
                                message.chat.id,
                                TIME_CHOICE,
                                reply_markup=choice_date()
                            )
                    except Exception as e:
                        print(e)
                        await bot.send_message(message.chat.id, "Спробуйте ще раз (формат через кому) : ")
                case 14:
                    if message.text == SKIP:
                        model_task_list["sub_desc"] = "\nОпис 2 : \nвідсутній"
                    else:
                        model_task_list["sub_desc"] = message.text
                    set_task_step(15)
                    await bot.send_message(
                        message.chat.id,
                        TIME_CHOICE,
                        reply_markup=choice_date()
                    )
                case 15:
                    try:
                        if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == SKIP:
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                        if model_task_list['count'] > 1:
                            sub_desc = f"\n{model_task_list['sub_desc']}\n"
                        else:
                            sub_desc = ""

                        desc_card = f"Кількість креативів : {model_task_list['count']}\n" \
                                    f"Гео : {model_task_list['geo']}\n" \
                                    f"Валюта : {model_task_list['valuta']}\n" \
                                    f"Формат : {model_task_list['format']}\n" \
                                    f"Оффер : {model_task_list['offer']}\n" \
                                    f"Назва слота чи тематики : {model_task_list['theme_name']}\n" \
                                    f"Емоції : {model_task_list['emotions']}\n" \
                                    f"Плашки : {model_task_list['tabs']}\n" \
                                    f"SMS : {model_task_list['sms']}\n" \
                                    f"Телефон із повідомленням : {model_task_list['phone_notify']}\n" \
                                    f"Назва банку : {model_task_list['name_bank']}\n" \
                                    f"Озвучка : {model_task_list['sound']}\n\n" \
                                    f"Опис : \n{model_task_list['desc']}\n{sub_desc}\n" \
                                    f"Зв'язок у тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"Order Creative by ({current_user.result.name_user})",
                            f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                            "cards_creo",
                            message.chat.id,
                        ).result

                        if result_add_to_db is not None:
                            card = card_id = create_card_creo(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} Креатив ({model_task_list['theme_name']})",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_creo,
                                date=dateTime
                            )
                            update_card(result_add_to_db['id'], card.json()['id'], "cards_creo")

                            add_attachments_to_card(
                                card_id=card_id.json()['id'],
                                source=model_task_list['reference']
                            )

                            if card_id.ok:
                                await bot.send_message(
                                    message.chat.id,
                                    MESSAGE_SEND,
                                    reply_markup=setStartButton()
                                )
                            else:
                                await bot.send_message(
                                    message.chat.id,
                                    MESSAGE_DONT_SEND,
                                    reply_markup=setStartButton()
                                )

                            set_state_none()  # reset user state
                        else:
                            await bot.send_message(
                                message.chat.id,
                                MESSAGE_DONT_SEND,
                                reply_markup=setStartButton()
                            )
                            set_state_none()  # reset user state

                    except Exception as e:
                        print(e)
                        if str(e).__contains__("does not match format '%Y-%m-%d %H:%M %z'"):
                            await bot.reply_to(
                                message,
                                WRONG_TIME_CHOICE
                            )
                        else:
                            set_state_none()  # reset user state
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "share_app")
async def share_app(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 2:
            match task_step["step"]:
                case 0:
                    model_task_list["name_app"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введіть ID кабінетів : ")
                case 1:
                    model_task_list["id_cabinets"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Введіть опис до завдання : ", reply_markup=skip_desc())
                case 2:
                    set_state_none()  # reset user state

                    if message.text == SKIP:
                        model_task_list["desc"] = ""
                    else:
                        model_task_list["desc"] = message.text

                    desc_card = f"Назва додатка : {model_task_list['name_app']}\n\n" \
                                f"ID кабінетів : \n{model_task_list['id_cabinets']}\n\n" \
                                f"Опис : \n{model_task_list['desc']}\n\n" \
                                f"Зв'язок у тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Share app by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Розшарити прілу ({model_task_list['name_app']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )
                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND, reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "other_task")
async def other_task(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 1:
            match task_step["step"]:
                case 0:
                    model_task_list["title"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введіть опис завдання : ")
                case 1:
                    model_task_list["desc"] = message.text
                    set_task_step(2)
                    await bot.send_message(
                        message.chat.id,
                        TIME_CHOICE,
                        reply_markup=choice_date()
                    )
                case 2:
                    try:
                        if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == SKIP:
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                        desc_card = f"{model_task_list['desc']}\n\n" \
                                    f"Зв'язок у тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"custom_task by ({current_user.result.name_user})",
                            f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                            "cards_tech",
                            message.chat.id,
                        ).result

                        if result_add_to_db is not None:
                            card = create_card_tech(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} {model_task_list['title']}",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_tech,
                                date=dateTime
                            )
                            update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                            await bot.send_message(message.chat.id, MESSAGE_SEND,
                                                   reply_markup=setStartButton())
                        else:
                            await bot.send_message(
                                message.chat.id,
                                MESSAGE_DONT_SEND,
                                reply_markup=setStartButton()
                            )

                        set_state_none()  # reset user state
                    except Exception as e:
                        print(e)
                        await bot.reply_to(
                            message,
                            WRONG_TIME_CHOICE
                        )
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "pwa_app")
async def pwa_(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 2:
            match task_step["step"]:
                case 0:
                    model_task_list["geo"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Назва програми : ")
                case 1:
                    model_task_list["name"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Опис завдання : ")
                case 2:
                    model_task_list["desc"] = message.text
                    set_task_step(3)
                    await bot.send_message(
                        message.chat.id,
                        TIME_CHOICE,
                        reply_markup=choice_date()
                    )
                case 3:
                    try:
                        if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == SKIP:
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                        desc_card = f"Гео : {model_task_list['geo']}\n" \
                                    f"Назва програми :  {model_task_list['name']}\n\n" \
                                    f"Опис : {model_task_list['desc']}\n\n" \
                                    f"Зв'язок у тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"PWA by ({current_user.result.name_user})",
                            f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                            "cards_tech",
                            message.chat.id,
                        ).result

                        if result_add_to_db is not None:
                            card = create_card_tech(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} Створити PWA додаток ({model_task_list['name']})",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_tech,
                                date=dateTime
                            )
                            update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                            await bot.send_message(message.chat.id, MESSAGE_SEND,
                                                   reply_markup=setStartButton())
                        else:
                            await bot.send_message(
                                message.chat.id,
                                MESSAGE_DONT_SEND,
                                reply_markup=setStartButton()
                            )

                        set_state_none()  # reset user state
                    except Exception as e:
                        print(e)
                        await bot.reply_to(
                            message,
                            WRONG_TIME_CHOICE
                        )

        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "add_comment")
async def add_comment(message):
    if get_user(message.chat.id).result is not None:
        try:
            if write_comment(id_card=model_task_list["current_card"], text=message.text):
                await bot.send_message(
                    message.chat.id,
                    "✅ Коментар доданий",
                    reply_markup=setStartButton()
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    "Помилка при додаванні коментарю",
                    reply_markup=setStartButton()
                )
        except:
            pass
        set_state_none()  # reset user state
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "create_campaign")
async def create_campaign(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match task_step["step"]:
                case 0:
                    model_task_list['geo'] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введіть прілу : ")
                case 1:
                    model_task_list['app_name'] = message.text

                    desc_card = f"Гео : {model_task_list['geo']}\n" \
                                f"Додаток : {model_task_list['app_name']}\n\n" \
                                f"Зв'язок у тг : @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Create campaign by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Створити кампанію ({model_task_list['app_name']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                        )
                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND,
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "set_domain")
async def set_domain(message):
    if get_user(message.chat.id).result is not None:
        match task_step["step"]:
            case 0:
                model_task_list['offer_names'] = message.text
                set_task_step(1)
                await bot.send_message(message.chat.id, "Введіть опис : ")

            case 1:
                model_task_list['desc'] = message.text
                set_task_step(2)
                await bot.send_message(
                    message.chat.id,
                    TIME_CHOICE,
                    reply_markup=choice_date()
                )

            case 2:
                try:
                    if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                   + datetime.timedelta(days=1)
                    elif message.text == SKIP:
                        dateTime = ""
                    else:
                        dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                    desc_card = f"Назви доменів : {model_task_list['offer_names']}\n\n" \
                                f"Опис : {model_task_list['desc']}\n\n" \
                                f"Зв'язок у тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Park domain by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Припаркувати домен",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                            date=dateTime
                        )
                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND,
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
                except Exception as e:
                    print(e)
                    await bot.reply_to(
                        message,
                        WRONG_TIME_CHOICE
                    )

    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "setting_cloak")
async def setting_cloak(message):
    if get_user(message.chat.id).result is not None:
        match task_step["step"]:
            case 0:
                model_task_list['geo'] = message.text
                set_task_step(1)
                await bot.send_message(message.chat.id, "Введіть оффер : ")
            case 1:
                model_task_list['offer'] = message.text
                set_task_step(2)
                await bot.send_message(message.chat.id, "Введіть домени : ")
            case 2:
                model_task_list['domains'] = message.text
                set_task_step(3)
                await bot.send_message(message.chat.id, "Введіть опис : ")
            case 3:
                model_task_list['desc'] = message.text
                set_task_step(4)
                await bot.send_message(
                    message.chat.id,
                    TIME_CHOICE,
                    reply_markup=choice_date()
                )

            case 4:
                try:
                    if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                   + datetime.timedelta(days=1)
                    elif message.text == SKIP:
                        dateTime = ""
                    else:
                        dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                    desc_card = f"Гео : {model_task_list['geo']}\n\n" \
                                f"Оффер : {model_task_list['offer']}\n\n" \
                                f"Домени : \n{model_task_list['domains']}\n\n" \
                                f"Опис : {model_task_list['desc']}\n\n" \
                                f"Зв'язок у тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Setting cloak by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Налаштувати клоаку",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                            date=dateTime
                        )
                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND,
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
                except Exception as e:
                    print(e)
                    await bot.reply_to(
                        message,
                        WRONG_TIME_CHOICE
                    )

    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "prepare_vait")
async def prepare_vait(message):
    if get_user(message.chat.id).result is not None:
        match task_step["step"]:
            case 0:
                model_task_list['geo'] = message.text
                set_task_step(1)
                await bot.send_message(message.chat.id, "Введіть вихідні дані : ")
            case 1:
                model_task_list['source'] = message.text
                set_task_step(2)
                await bot.send_message(message.chat.id, "Введіть ТЗ/посилання на ТЗ : ")
            case 2:
                model_task_list['link_tt'] = message.text
                set_task_step(3)
                await bot.send_message(message.chat.id, "Введіть опис : ")
            case 3:
                model_task_list['desc'] = message.text
                set_task_step(4)
                await bot.send_message(
                    message.chat.id,
                    TIME_CHOICE,
                    reply_markup=choice_date()
                )

            case 4:
                try:
                    if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                   + datetime.timedelta(days=1)
                    elif message.text == SKIP:
                        dateTime = ""
                    else:
                        dateTime = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                    desc_card = f"Гео : {model_task_list['geo']}\n" \
                                f"Джерело : {model_task_list['source']}\n\n" \
                                f"ТЗ : \n{model_task_list['link_tt']}\n\n" \
                                f"Опис : {model_task_list['desc']}\n\n" \
                                f"Зв'язок у тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Prepare vait by ({current_user.result.name_user})",
                        f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                        "cards_tech",
                        message.chat.id,
                    ).result

                    if result_add_to_db is not None:
                        card = create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Підготувати вайт",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                            date=dateTime
                        )
                        update_card(result_add_to_db['id'], card.json()['id'], "cards_tech")
                        await bot.send_message(message.chat.id, MESSAGE_SEND,
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
                except Exception as e:
                    print(e)
                    await bot.reply_to(
                        message,
                        WRONG_TIME_CHOICE
                    )

    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in (
        "edit_offer", "add_offer", "order_creative", "share_app", "other_task",
        "pwa_app", "create_campaign", "set_domain", "setting_cloak", "prepare_vait",
        "my_task_creo", "my_task_tech", "standard_creo", "gambling_creo"))
async def answer(call):
    global user_state
    set_state_none()  # reset user state

    reset_task_list()

    current_user = get_user(call.from_user.id).result

    if current_user is not None:
        match call.data:
            case "edit_offer":
                if current_user.dep_user in ("afmngr", "admin"):
                    user_state = "edit_offer"
                    await bot.send_message(
                        call.from_user.id,
                        "Id оффера у трекері : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "add_offer":
                if current_user.dep_user in ("afmngr", "admin"):
                    user_state = "add_offer"
                    await bot.send_message(
                        call.from_user.id,
                        "Новий рекламодавець чи існуючий?",
                        reply_markup=choice_offer_type()
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "order_creative":
                if current_user.dep_user != "afmngr":
                    if current_user.dep_user in ("gambleppc", "gambleuac", "gamblefb", "admin"):
                        await bot.send_message(
                            call.from_user.id,
                            "Виберіть тип креативу : ",
                            reply_markup=choice_type_creo()
                        )

                    else:
                        user_state = "order_creative"

                        await bot.send_message(
                            call.from_user.id,
                            "Мова, валюта: (наприклад: CAD/або символ валюти) : ",
                            reply_markup=close_markup
                        )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "standard_creo":
                if current_user.dep_user != "afmngr":
                    user_state = "order_creative"

                    await bot.send_message(
                        call.from_user.id,
                        "Мова, валюта: (наприклад: CAD/або символ валюти) : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )

            case "gambling_creo":
                if current_user.dep_user in ("gambleppc", "gambleuac", "gamblefb", "admin"):
                    user_state = "order_creative_gamble"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть кількість креативів : ",
                        reply_markup=close_markup
                    )

                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "share_app":
                if current_user.dep_user in ("gamblefb", "gambleuac", "admin"):
                    user_state = "share_app"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть назву програми : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "other_task":
                if current_user.dep_user in ("gamblefb", "gambleuac", "gambleppc", "admin"):
                    user_state = "other_task"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть коротку назву завдання : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "pwa_app":
                if current_user.dep_user in ("gamblefb", "gambleuac", "admin"):
                    user_state = "pwa_app"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "create_campaign":
                if current_user.dep_user in ("gamblefb", "gambleuac", "gambleppc", "admin"):
                    user_state = "create_campaign"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "set_domain":
                if current_user.dep_user in ("gambleppc", "admin"):
                    user_state = "set_domain"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть назви доменів : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "setting_cloak":
                if current_user.dep_user in ("gambleppc", "admin"):
                    user_state = "setting_cloak"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "prepare_vait":
                if current_user.dep_user in ("gambleppc", "admin"):
                    user_state = "prepare_vait"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "my_task_creo":
                creo_tasks = get_tasks(typeListId=idList_creo, userlabel=current_user.label_creo)
                if creo_tasks.markup is None:
                    await bot.send_message(call.from_user.id, creo_tasks.message)
                else:
                    await bot.send_message(call.from_user.id, "Ваші завдання creo : ", reply_markup=creo_tasks.markup)

            case "my_task_tech":
                creo_tasks = get_tasks(typeListId=idList_tech, userlabel=current_user.label_tech)
                if creo_tasks.markup is None:
                    await bot.send_message(call.from_user.id, creo_tasks.message)
                else:
                    await bot.send_message(call.from_user.id, "Ваші завдання tech : ", reply_markup=creo_tasks.markup)
    else:
        await bot.send_message(call.from_user.id, NOT_REGISTERED_USER,
                               reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in get_callback_cards() + ["delete_card", "commend_card"])
async def answer_cards(call):
    global user_state
    set_state_none()  # reset user state

    match call.data:
        case "delete_card":
            try:
                if delete_card(id_card=model_task_list["current_card"]):
                    await bot.send_message(call.from_user.id, "✅ Завдання видалено з Trello")
                else:
                    await bot.send_message(call.from_user.id, "Помилка при видаленні")
            except:
                pass
        case "commend_card":
            user_state = "add_comment"

            await bot.send_message(
                call.from_user.id,
                "Введіть коментар : ",
                reply_markup=close_markup
            )
        case _:
            card = get_card(call.data.replace("card_", ""))
            model_task_list["current_card"] = card.id
            await bot.send_message(
                call.from_user.id,
                f"<b>{card.name}</b>\n{'=' * len(card.name)}\n{card.desc}",
                parse_mode="Html",
                reply_markup=manage_card()
            )


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
