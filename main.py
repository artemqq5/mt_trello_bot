import datetime
from telebot import types

from bot_helper.af_manager_buttons import af_manager_menu, choice_offer_type
from bot_helper.gambling_fb_buttons import gambling_fb_menu
from bot_helper.gambling_ppc_buttons import gambling_ppc_menu
from bot_helper.gambling_uac_buttons import gambling_uac_menu
from bot_helper.media_buttons import media_menu
from config import DEBUG_MODE
from db_helper.db_manager import add_user, User, delete_user, get_user, get_list_users, add_card
from bot_helper.menu_buttons import setStartButton, choice_date, skip_desc, my_tasks_menu, manage_card
from models.task_form import *
from private_config import local_telegram_token, server_telegram_token
from telebot.async_telebot import AsyncTeleBot
import asyncio

from trello_helper.trello_manager import create_card_tech, TrelloCard, create_label, create_card_creo, \
    add_attachments_to_card, get_tasks, idList_creo, get_callback_cards, get_card, idList_tech, delete_card, \
    write_comment

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
dep_states = {"admin", "gamble_ppc", "gamble_uac", "gamble_fb", "af_manager", "media"}

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

    if get_user(message.chat.id).result is not None:
        await bot.send_message(message.chat.id, 'Меню', reply_markup=setStartButton())
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


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
                    'Введите пользователя формат id name dep : ',
                    reply_markup=close_markup
                )
            elif message.text == '/delete_user':
                user_state = "delete_user"
                await bot.send_message(message.chat.id, 'Введите id пользователя : ', reply_markup=close_markup)
            elif message.text == '/mailing_all':
                user_state = "mailing_all"
                await bot.send_message(
                    message.chat.id,
                    'Введите сообщение для рассылки всем пользователям : ',
                    reply_markup=close_markup
                )
        else:
            await bot.send_message(message.chat.id, 'У вас нет доступа, напишите админу', reply_markup=close_markup)
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state in ("add_user", "delete_user"))
async def user_delete_add(message):
    if get_user(message.chat.id).result is not None:
        if user_state == "add_user":
            listDataUser = message.text.split(" ")
            if len(listDataUser) == 3:
                if listDataUser[2] in dep_states:
                    if get_user(listDataUser[0]).result is not None:
                        set_state_none()  # reset user state
                        await bot.reply_to(message, 'Пользователь уже в базе', reply_markup=setStartButton())
                    else:
                        if add_user(User(
                                listDataUser[0],
                                listDataUser[1],
                                listDataUser[2],
                                create_label(listDataUser[1], "tech")["id"],
                                create_label(listDataUser[1], "creo")["id"])).result:
                            set_state_none()  # reset user state
                            await bot.reply_to(message, 'Пользователь добавлен', reply_markup=setStartButton())
                        else:
                            await bot.reply_to(message, 'Ошибка ввода. Используйте формат id name dep :')
                else:
                    await bot.reply_to(message, f'Такого dep нет. Используйте один из {tuple(dep_states)} :')
            else:
                await bot.reply_to(message, 'Ошибка ввода. Используйте формат id name dep :')
        elif user_state == "delete_user":
            if get_user(message.text).result is not None:
                set_state_none()  # reset user state

                if delete_user(message.text).result:
                    await bot.reply_to(message, 'Пользователь успешно удален', reply_markup=setStartButton())
                else:
                    await bot.reply_to(
                        message,
                        'Не вышло удалить пользователя, напишите админу',
                        reply_markup=setStartButton()
                    )
            else:
                await bot.reply_to(message, 'Такого пользователя нет в базе, повторите попытку :')
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


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
            f"📬 Успешно доставлено {len(users.result) - unsuccessful} пользователям из {len(users.result)}",
            reply_markup=setStartButton()
        )
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(
    func=lambda m: m.text in ("Gambling FB", "Gambling PPC", "Gambling UAC", "AF Manager", "Media", "Мои Задания 📋"))
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
            case "Мои Задания 📋":
                await bot.send_message(message.chat.id, message.text + " : ", reply_markup=my_tasks_menu())
            case _:
                await bot.reply_to(message, "(В разработке)")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "add_offer")
async def offer_add(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match task_step["step"]:
                case 0:
                    match message.text:
                        case "Новый":
                            model_task_list["type"] = "Новый"
                            model_task_list["operation"] = "Добавить новый оффер"
                            set_task_step(1)
                            await bot.send_message(message.chat.id, "Группа в тг :", reply_markup=close_markup)
                        case "Существующий":
                            model_task_list["type"] = "Существующий"
                            model_task_list["operation"] = "Добавить существующий оффер"
                            set_task_step(2)
                            await bot.send_message(message.chat.id, "Имя рекламодателя :", reply_markup=close_markup)
                        case _:
                            await bot.reply_to(message, "Выберите из (Новый или Существующий)")
                case 1:
                    model_task_list["tg_group"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Имя рекламодателя :")
                case 2:
                    model_task_list["adv_name"] = message.text
                    set_task_step(3)
                    await bot.send_message(message.chat.id, "Название оффера :")
                case 3:
                    model_task_list["offer_name"] = message.text
                    set_task_step(4)
                    await bot.send_message(message.chat.id, "Гео :")
                case 4:
                    model_task_list["geo"] = message.text
                    set_task_step(5)
                    await bot.send_message(message.chat.id, "Отчисление по гео :")
                case 5:
                    model_task_list["reward_geo"] = message.text
                    set_task_step(6)
                    await bot.send_message(message.chat.id, "Промо ссылка :")
                case 6:
                    set_state_none()  # reset user state
                    model_task_list["promo_link"] = message.text

                    if model_task_list["type"] == "Существующий":
                        tg_group = ""
                    else:
                        tg_group = f"Группа в тг: {model_task_list['tg_group']}\n"

                    desc_card = f"Тип: {model_task_list['type']}\n" \
                                f"{tg_group}" \
                                f"Имя рекламодателя: {model_task_list['adv_name']}\n" \
                                f"Название оффера: {model_task_list['offer_name']}\n" \
                                f"Гео: {model_task_list['geo']}\n" \
                                f"Отчисление по гео: {model_task_list['reward_geo']}\n" \
                                f"Промо ссылка: {model_task_list['promo_link']}\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Добавить {model_task_list['type']} оффер {current_user.result.name_user}",
                        model_task_list['offer_name'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} {model_task_list['operation']} ({model_task_list['offer_name']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!", reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "edit_offer")
async def offer_edit(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match task_step["step"]:
                case 0:
                    model_task_list["operation"] = "Редактировать оффер"
                    model_task_list["offer_id"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введите описание что сделать : ")
                case 1:
                    set_state_none()  # reset user state

                    model_task_list["desc_offer"] = message.text

                    desc_card = f"Id оффера в трекере : {model_task_list['offer_id']}\n" \
                                f"Задача : {model_task_list['desc_offer']}\n\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Редактировать оффер {current_user.result.name_user}",
                        model_task_list['offer_id'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} {model_task_list['operation']} ({model_task_list['offer_id']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!", reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "order_creative")
async def order_creo(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] in (4, 8):
            match task_step["step"]:
                case 0:
                    model_task_list["currency_type"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введите гео : ")
                case 1:
                    model_task_list["geo"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Введите тайминг видео (в секундах) : ")
                case 2:
                    model_task_list["timing_video"] = message.text
                    set_task_step(3)
                    await bot.send_message(
                        message.chat.id,
                        "Формат креатива: размер (например 1000х1000 пикселей) ,"
                        " формат файла (например mp4), необходимый размер файла (например до 10 мб):"
                    )
                case 3:
                    model_task_list["format"] = message.text
                    set_task_step(4)
                    await bot.send_message(
                        message.chat.id,
                        "Вложения для ТЗ: ссылки на картинки/видео через запятую"
                        "Например: \nhttps://google.com/,https://google.com/"
                    )
                case 4:
                    try:
                        model_task_list["source"] = message.text.split(",")
                        set_task_step(5)
                        await bot.send_message(message.chat.id, "Введите количество креативов : ")
                    except Exception as e:
                        print(e)
                        await bot.send_message(message.chat.id, "Попробуйте еще раз (формат через запятую) : ")
                case 5:
                    model_task_list["count"] = message.text
                    set_task_step(6)
                    await bot.send_message(message.chat.id, "Введите оффер : ")
                case 6:
                    model_task_list["offer"] = message.text
                    set_task_step(7)
                    await bot.send_message(message.chat.id, "Введите описание : ")
                case 7:
                    model_task_list["desc"] = message.text
                    set_task_step(8)
                    await bot.send_message(message.chat.id, "Введите краткое название для карты : ")
                case 8:
                    if len(message.text) <= 40:
                        model_task_list["title"] = message.text
                        set_task_step(9)
                        await bot.send_message(
                            message.chat.id,
                            "Введите дедлайн задачи в формате\n"
                            "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                            reply_markup=choice_date()
                        )
                    else:
                        await bot.reply_to(message, "Краткое название должно быть до 40 символов : ")
                case 9:
                    try:
                        if message.text in ("Сегодня 12:00", "Сегодня 15:00", "Сегодня 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z')
                        elif message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == "Пропустить":
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0200", '%Y-%m-%d %H:%M %z')

                        desc_card = f"Валюта : {model_task_list['currency_type']}\n" \
                                    f"Гео : {model_task_list['geo']}\n" \
                                    f"Тайминг видео : {model_task_list['timing_video']}\n" \
                                    f"Формат креатива : {model_task_list['format']}\n" \
                                    f"Количество креативов : {model_task_list['count']}\n" \
                                    f"Оффер : {model_task_list['offer']}\n\n" \
                                    f"Описание доп : \n{model_task_list['desc']}\n\n" \
                                    f"Связь в тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"Заказать Креатив {current_user.result.name_user}",
                            model_task_list['title'],
                            "cards_creo"
                        ).result

                        if result_add_to_db is not None:
                            card_id = create_card_creo(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} Заказать Креатив ({model_task_list['title']})",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_creo,
                                date=dateTime
                            )

                            result = add_attachments_to_card(card_id=card_id.json()['id'],
                                                             source=model_task_list['source'])

                            if card_id.ok and result:
                                await bot.send_message(
                                    message.chat.id,
                                    "✅ Задание отправленно!",
                                    reply_markup=setStartButton()
                                )
                            else:
                                await bot.send_message(
                                    message.chat.id,
                                    "Не вышло отправить задание",
                                    reply_markup=setStartButton()
                                )

                            set_state_none()  # reset user state
                        else:
                            await bot.send_message(
                                message.chat.id,
                                "Не вышло отправить задание",
                                reply_markup=setStartButton()
                            )
                            set_state_none()  # reset user state

                    except Exception as e:
                        print(e)
                        await bot.reply_to(
                            message,
                            "Неправильный формат, введите в формате\n"
                            "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00"
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "share_app")
async def share_app(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 2:
            match task_step["step"]:
                case 0:
                    model_task_list["name_app"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введите ID кабинетов : ")
                case 1:
                    model_task_list["id_cabinets"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Введите описание к задаче : ", reply_markup=skip_desc())
                case 2:
                    set_state_none()  # reset user state

                    if message.text == "Пропустить":
                        model_task_list["desc"] = ""
                    else:
                        model_task_list["desc"] = message.text

                    desc_card = f"Название приложения : {model_task_list['name_app']}\n\n" \
                                f"ID кабинетов : \n{model_task_list['id_cabinets']}\n\n" \
                                f"Описание : \n{model_task_list['desc']}\n\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Расшарить прилу {current_user.result.name_user}",
                        model_task_list['desc'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Расшарить прилу ({model_task_list['name_app']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!", reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "other_task")
async def other_task(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 1:
            match task_step["step"]:
                case 0:
                    model_task_list["title"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введите описание задачи : ")
                case 1:
                    model_task_list["desc"] = message.text
                    set_task_step(2)
                    await bot.send_message(
                        message.chat.id,
                        "Введите дедлайн задачи в формате\n"
                        "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                        reply_markup=choice_date()
                    )
                case 2:
                    try:
                        if message.text in ("Сегодня 12:00", "Сегодня 15:00", "Сегодня 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z')
                        elif message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == "Пропустить":
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0200", '%Y-%m-%d %H:%M %z')

                        desc_card = f"{model_task_list['desc']}\n\n" \
                                    f"Связь в тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"custom_task {current_user.result.name_user}",
                            model_task_list['title'],
                            "cards_tech"
                        ).result

                        if result_add_to_db is not None:
                            create_card_tech(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} {model_task_list['title']}",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_tech,
                                date=dateTime
                            )
                            await bot.send_message(message.chat.id, "✅ Задание отправленно!",
                                                   reply_markup=setStartButton())
                        else:
                            await bot.send_message(
                                message.chat.id,
                                "Не вышло отправить задание",
                                reply_markup=setStartButton()
                            )

                        set_state_none()  # reset user state
                    except Exception as e:
                        print(e)
                        await bot.reply_to(
                            message,
                            "Неправильный формат, введите в формате\n"
                            "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00"
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "pwa_app")
async def pwa_(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 2:
            match task_step["step"]:
                case 0:
                    model_task_list["geo"] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Название приложения : ")
                case 1:
                    model_task_list["name"] = message.text
                    set_task_step(2)
                    await bot.send_message(message.chat.id, "Описание задачи : ")
                case 2:
                    model_task_list["desc"] = message.text
                    set_task_step(3)
                    await bot.send_message(
                        message.chat.id,
                        "Введите дедлайн задачи в формате\n"
                        "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                        reply_markup=choice_date()
                    )
                case 3:
                    try:
                        if message.text in ("Сегодня 12:00", "Сегодня 15:00", "Сегодня 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z')
                        elif message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                            dateTime = datetime.datetime.strptime(
                                datetime.datetime.now().strftime("%Y-%m-%d") +
                                " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z') \
                                       + datetime.timedelta(days=1)
                        elif message.text == "Пропустить":
                            dateTime = ""
                        else:
                            dateTime = datetime.datetime.strptime(message.text + " +0200", '%Y-%m-%d %H:%M %z')

                        desc_card = f"Гео : {model_task_list['geo']}\n" \
                                    f"Название приложения :  {model_task_list['name']}\n\n" \
                                    f"Описание : {model_task_list['desc']}\n\n" \
                                    f"Связь в тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(
                            f"PWA {current_user.result.name_user}",
                            model_task_list['desc'],
                            "cards_tech"
                        ).result

                        if result_add_to_db is not None:
                            create_card_tech(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} Создать PWA приложение ({model_task_list['name']})",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_tech,
                                date=dateTime
                            )
                            await bot.send_message(message.chat.id, "✅ Задание отправленно!",
                                                   reply_markup=setStartButton())
                        else:
                            await bot.send_message(
                                message.chat.id,
                                "Не вышло отправить задание",
                                reply_markup=setStartButton()
                            )

                        set_state_none()  # reset user state
                    except Exception as e:
                        print(e)
                        await bot.reply_to(
                            message,
                            "Неправильный формат, введите в формате\n"
                            "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00"
                        )

        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "add_comment")
async def add_comment(message):
    if get_user(message.chat.id).result is not None:
        try:
            if write_comment(id_card=model_task_list["current_card"], text=message.text):
                await bot.send_message(
                    message.chat.id,
                    "✅ Комментарий добавлен",
                    reply_markup=setStartButton()
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    "Ошибка при добавлении комментария",
                    reply_markup=setStartButton()
                )
        except:
            pass
        set_state_none()  # reset user state
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "create_campaign")
async def create_campaign(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match task_step["step"]:
                case 0:
                    model_task_list['geo'] = message.text
                    set_task_step(1)
                    await bot.send_message(message.chat.id, "Введите оффер : ")
                case 1:
                    model_task_list['offer_name'] = message.text

                    desc_card = f"Гео : {model_task_list['geo']}\n" \
                                f"Оффер : {model_task_list['offer_name']}\n\n" \
                                f"Связь в тг : @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Создать кампанию {current_user.result.name_user}",
                        model_task_list['offer_name'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Создать кампанию ({model_task_list['offer_name']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!",
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "set_domain")
async def set_domain(message):
    if get_user(message.chat.id).result is not None:
        match task_step["step"]:
            case 0:
                model_task_list['offer_names'] = message.text
                set_task_step(1)
                await bot.send_message(message.chat.id, "Введите описание : ")

            case 1:
                model_task_list['desc'] = message.text
                set_task_step(2)
                await bot.send_message(
                    message.chat.id,
                    "Введите дедлайн задачи в формате\n"
                    "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                    reply_markup=choice_date()
                )

            case 2:
                try:
                    if message.text in ("Сегодня 12:00", "Сегодня 15:00", "Сегодня 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z')
                    elif message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z') \
                                   + datetime.timedelta(days=1)
                    elif message.text == "Пропустить":
                        dateTime = ""
                    else:
                        dateTime = datetime.datetime.strptime(message.text + " +0200", '%Y-%m-%d %H:%M %z')

                    desc_card = f"Названия доменов : {model_task_list['offer_names']}\n\n" \
                                f"Описание : {model_task_list['desc']}\n\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Припарковать домен {current_user.result.name_user}",
                        model_task_list['desc'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Припарковать домен",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                            date=dateTime
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!",
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
                except Exception as e:
                    print(e)
                    await bot.reply_to(
                        message,
                        "Неправильный формат, введите в формате\n"
                        "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00"
                    )

    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "setting_cloak")
async def setting_cloak(message):
    if get_user(message.chat.id).result is not None:
        match task_step["step"]:
            case 0:
                model_task_list['geo'] = message.text
                set_task_step(1)
                await bot.send_message(message.chat.id, "Введите оффер : ")
            case 1:
                model_task_list['offer'] = message.text
                set_task_step(2)
                await bot.send_message(message.chat.id, "Введите домены : ")
            case 2:
                model_task_list['domains'] = message.text
                set_task_step(3)
                await bot.send_message(message.chat.id, "Введите описание : ")
            case 3:
                model_task_list['desc'] = message.text
                set_task_step(4)
                await bot.send_message(
                    message.chat.id,
                    "Введите дедлайн задачи в формате\n"
                    "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                    reply_markup=choice_date()
                )

            case 4:
                try:
                    if message.text in ("Сегодня 12:00", "Сегодня 15:00", "Сегодня 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z')
                    elif message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z') \
                                   + datetime.timedelta(days=1)
                    elif message.text == "Пропустить":
                        dateTime = ""
                    else:
                        dateTime = datetime.datetime.strptime(message.text + " +0200", '%Y-%m-%d %H:%M %z')

                    desc_card = f"Гео : {model_task_list['geo']}\n\n" \
                                f"Оффер : {model_task_list['offer']}\n\n" \
                                f"Домены : \n{model_task_list['domains']}\n\n" \
                                f"Описание : {model_task_list['desc']}\n\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Настроить клоаку {current_user.result.name_user}",
                        model_task_list['desc'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Настроить клоаку",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                            date=dateTime
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!",
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
                except Exception as e:
                    print(e)
                    await bot.reply_to(
                        message,
                        "Неправильный формат, введите в формате\n"
                        "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00"
                    )

    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "prepare_vait")
async def prepare_vait(message):
    if get_user(message.chat.id).result is not None:
        match task_step["step"]:
            case 0:
                model_task_list['geo'] = message.text
                set_task_step(1)
                await bot.send_message(message.chat.id, "Введите исходники : ")
            case 1:
                model_task_list['source'] = message.text
                set_task_step(2)
                await bot.send_message(message.chat.id, "Введите ТЗ / ссылку на ТЗ : ")
            case 2:
                model_task_list['link_tt'] = message.text
                set_task_step(3)
                await bot.send_message(message.chat.id, "Введите описание : ")
            case 3:
                model_task_list['desc'] = message.text
                set_task_step(4)
                await bot.send_message(
                    message.chat.id,
                    "Введите дедлайн задачи в формате\n"
                    "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                    reply_markup=choice_date()
                )

            case 4:
                try:
                    if message.text in ("Сегодня 12:00", "Сегодня 15:00", "Сегодня 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z')
                    elif message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                        dateTime = datetime.datetime.strptime(
                            datetime.datetime.now().strftime("%Y-%m-%d") +
                            " " + message.text.split(" ")[1] + " +0200", '%Y-%m-%d %H:%M %z') \
                                   + datetime.timedelta(days=1)
                    elif message.text == "Пропустить":
                        dateTime = ""
                    else:
                        dateTime = datetime.datetime.strptime(message.text + " +0200", '%Y-%m-%d %H:%M %z')

                    desc_card = f"Гео : {model_task_list['geo']}\n" \
                                f"Исходники : {model_task_list['source']}\n\n" \
                                f"ТЗ : \n{model_task_list['link_tt']}\n\n" \
                                f"Описание : {model_task_list['desc']}\n\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(
                        f"Подготовить вайт {current_user.result.name_user}",
                        model_task_list['desc'],
                        "cards_tech"
                    ).result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} Подготовить вайт",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech,
                            date=dateTime
                        )
                        await bot.send_message(message.chat.id, "✅ Задание отправленно!",
                                               reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )

                    set_state_none()  # reset user state
                except Exception as e:
                    print(e)
                    await bot.reply_to(
                        message,
                        "Неправильный формат, введите в формате\n"
                        "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00"
                    )

    else:
        await bot.send_message(message.chat.id, '⛔ Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in (
        "edit_offer", "add_offer", "order_creative", "share_app", "other_task",
        "pwa_app", "create_campaign", "set_domain", "setting_cloak", "prepare_vait", "my_task_creo", "my_task_tech"))
async def answer(call):
    global user_state
    set_state_none()  # reset user state

    reset_task_list()

    current_user = get_user(call.from_user.id).result

    if current_user is not None:
        match call.data:
            case "edit_offer":
                user_state = "edit_offer"

                await bot.send_message(
                    call.from_user.id,
                    "Id оффера в трекере : ",
                    reply_markup=close_markup
                )
            case "add_offer":
                user_state = "add_offer"

                await bot.send_message(
                    call.from_user.id,
                    "Новый рекламодатель или существующий?",
                    reply_markup=choice_offer_type()
                )
            case "order_creative":
                user_state = "order_creative"

                await bot.send_message(
                    call.from_user.id,
                    "Язык, валюта: (например: CAD/или символ валюты) : ",
                    reply_markup=close_markup
                )
            case "share_app":
                user_state = "share_app"

                await bot.send_message(
                    call.from_user.id,
                    "Введите название приложения : ",
                    reply_markup=close_markup
                )
            case "other_task":
                user_state = "other_task"

                await bot.send_message(
                    call.from_user.id,
                    "Введите краткое название задачи : ",
                    reply_markup=close_markup
                )
            case "pwa_app":
                user_state = "pwa_app"

                await bot.send_message(
                    call.from_user.id,
                    "Гео : ",
                    reply_markup=close_markup
                )
            case "create_campaign":
                user_state = "create_campaign"

                await bot.send_message(
                    call.from_user.id,
                    "Гео : ",
                    reply_markup=close_markup
                )
            case "set_domain":
                user_state = "set_domain"

                await bot.send_message(
                    call.from_user.id,
                    "Введите названия доменов : ",
                    reply_markup=close_markup
                )
            case "setting_cloak":
                user_state = "setting_cloak"

                await bot.send_message(
                    call.from_user.id,
                    "Гео : ",
                    reply_markup=close_markup
                )
            case "prepare_vait":
                user_state = "prepare_vait"

                await bot.send_message(
                    call.from_user.id,
                    "Гео : ",
                    reply_markup=close_markup
                )
            case "my_task_creo":
                creo_tasks = get_tasks(typeListId=idList_creo, userlabel=current_user.label_creo)
                if creo_tasks.markup is None:
                    await bot.send_message(call.from_user.id, creo_tasks.message)
                else:
                    await bot.send_message(call.from_user.id, "Ваши задания creo : ", reply_markup=creo_tasks.markup)

            case "my_task_tech":
                creo_tasks = get_tasks(typeListId=idList_tech, userlabel=current_user.label_tech)
                if creo_tasks.markup is None:
                    await bot.send_message(call.from_user.id, creo_tasks.message)
                else:
                    await bot.send_message(call.from_user.id, "Ваши задания tech : ", reply_markup=creo_tasks.markup)
    else:
        await bot.send_message(call.from_user.id, '⛔ Вы не зарегестрированы, напишите админу',
                               reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in get_callback_cards() + ["delete_card", "commend_card"])
async def answer_cards(call):
    global user_state
    set_state_none()  # reset user state

    match call.data:
        case "delete_card":
            try:
                if delete_card(id_card=model_task_list["current_card"]):
                    await bot.send_message(call.from_user.id, "✅ Задание удаленно из Trello")
                else:
                    await bot.send_message(call.from_user.id, "Ошибка при удалении")
            except:
                pass
        case "commend_card":
            user_state = "add_comment"

            await bot.send_message(
                call.from_user.id,
                "Введите комментарий : ",
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
