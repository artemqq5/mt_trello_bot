import datetime

from telebot import types

from config import DEBUG_MODE
from db_helper.db_manager import add_user, User, delete_user, get_user, get_list_users, add_card
from bot_helper.menu_buttons import setStartButton, af_manager_menu, choice_offer_type, media_menu, \
    choice_media_type_date
from models.af_manager_model import model_offer, offer_step, set_offer_step, reset_offer
from models.media_manager_model import reset_media, set_media_step, media_step, model_media
from private_config import local_telegram_token, server_telegram_token
from telebot.async_telebot import AsyncTeleBot
import asyncio

from trello_helper.trello_manager import create_card_tech, TrelloCard, create_label, create_card_creo

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
    "edit_offer"

    "order_creative"
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
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


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
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


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
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


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
            f"Успешно доставлено {len(users.result) - unsuccessful} пользователям из {len(users.result)}",
            reply_markup=setStartButton()
        )
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(
    func=lambda m: m.text in ("Gambling FB", "Gambling PPC", "Gambling UAC", "AF Manager", "Schema", "Media"))
async def choice_category(message):
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        match message.text:
            case "AF Manager":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=af_manager_menu())
            case "Media":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=media_menu())
            case _:
                await bot.reply_to(message, "(В разработке)")
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "add_offer")
async def offer_add(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match offer_step["step"]:
                case 0:
                    match message.text:
                        case "Новый":
                            model_offer["type"] = "Новый"
                            model_offer["operation"] = "Добавить новый оффер"
                            set_offer_step(1)
                            await bot.send_message(message.chat.id, "Группа в тг :", reply_markup=close_markup)
                        case "Существующий":
                            model_offer["type"] = "Существующий"
                            model_offer["operation"] = "Добавить существующий оффер"
                            set_offer_step(2)
                            await bot.send_message(message.chat.id, "Имя рекламодателя :", reply_markup=close_markup)
                        case _:
                            await bot.reply_to(message, "Выберите из (Новый или Существующий)")
                case 1:
                    model_offer["tg_group"] = message.text
                    set_offer_step(2)
                    await bot.send_message(message.chat.id, "Имя рекламодателя :")
                case 2:
                    model_offer["adv_name"] = message.text
                    set_offer_step(3)
                    await bot.send_message(message.chat.id, "Название оффера :")
                case 3:
                    model_offer["offer_name"] = message.text
                    set_offer_step(4)
                    await bot.send_message(message.chat.id, "Гео :")
                case 4:
                    model_offer["geo"] = message.text
                    set_offer_step(5)
                    await bot.send_message(message.chat.id, "Отчисление по гео :")
                case 5:
                    model_offer["reward_geo"] = message.text
                    set_offer_step(6)
                    await bot.send_message(message.chat.id, "Промо ссылка :")
                case 6:
                    set_state_none()  # reset user state
                    model_offer["promo_link"] = message.text

                    if model_offer["type"] == "Существующий":
                        tg_group = ""
                    else:
                        tg_group = f"Группа в тг: {model_offer['tg_group']}\n"

                    desc_card = f"Тип: {model_offer['type']}\n" \
                                f"{tg_group}" \
                                f"Имя рекламодателя: {model_offer['adv_name']}\n" \
                                f"Название оффера: {model_offer['offer_name']}\n" \
                                f"Гео: {model_offer['geo']}\n" \
                                f"Отчисление по гео: {model_offer['reward_geo']}\n" \
                                f"Промо ссылка: {model_offer['promo_link']}\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(model_offer['offer_name'], desc_card, "cards_tech").result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} {model_offer['operation']} ({model_offer['offer_name']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )
                        await bot.send_message(message.chat.id, "Задание отправленно!", reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "edit_offer")
async def offer_edit(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match offer_step["step"]:
                case 0:
                    model_offer["offer_id"] = message.text
                    set_offer_step(1)
                    await bot.send_message(message.chat.id, "Введите описание что сделать : ")
                case 1:
                    set_state_none()  # reset user state

                    model_offer["desc_offer"] = message.text

                    desc_card = f"Id оффера в трекере : {model_offer['offer_id']}\n" \
                                f"Задача : {model_offer['desc_offer']}\n\n" \
                                f"Связь в тг: @{message.chat.username}\n"

                    current_user = get_user(message.chat.id)
                    result_add_to_db = add_card(model_offer['offer_id'], desc_card, "cards_tech").result

                    if result_add_to_db is not None:
                        create_card_tech(
                            TrelloCard(
                                name=f"#{result_add_to_db['id']} {model_offer['operation']} ({model_offer['offer_id']})",
                                desc=desc_card
                            ),
                            owner_dep=current_user.result.dep_user,
                            owner_name=current_user.result.label_tech
                        )
                        await bot.send_message(message.chat.id, "Задание отправленно!", reply_markup=setStartButton())
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "Не вышло отправить задание",
                            reply_markup=setStartButton()
                        )
        else:
            await bot.reply_to(message, "Введите строку до 100 символов")
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state == "order_creative")
async def order_creo(message):
    if get_user(message.chat.id).result is not None:
        if len(message.text) < 100:
            match media_step["step"]:
                case 0:
                    model_media["currency_type"] = message.text
                    set_media_step(1)
                    await bot.send_message(message.chat.id, "Введите гео : ")
                case 1:
                    model_media["geo"] = message.text
                    set_media_step(2)
                    await bot.send_message(message.chat.id, "Введите тайминг видео (в секундах) : ")
                case 2:
                    model_media["timing_video"] = message.text
                    set_media_step(3)
                    await bot.send_message(
                        message.chat.id,
                        "Формат креатива: размер (например 1000х1000 пикселей) ,"
                        " формат файла (например mp4), необходимый размер файла (например до 10 мб):"
                    )
                case 3:
                    model_media["format"] = message.text
                    set_media_step(4)
                    await bot.send_message(
                        message.chat.id,
                        "Вложения для ТЗ: ссылки на картинки/видео и объяснение! Брать ли исходники"
                        " на усмотрение креативщика либо опишите как именно использовать референсы в креативе."
                    )
                case 4:
                    model_media["source"] = message.text
                    set_media_step(5)
                    await bot.send_message(message.chat.id, "Введите количество креативов : ")
                case 5:
                    model_media["count"] = message.text
                    set_media_step(6)
                    await bot.send_message(message.chat.id, "Введите оффер : ")
                case 6:
                    model_media["offer"] = message.text
                    set_media_step(7)
                    await bot.send_message(message.chat.id, "Введите описание : ")
                case 7:
                    model_media["desc"] = message.text
                    set_media_step(8)
                    await bot.send_message(message.chat.id, "Введите краткое название для карты : ")
                case 8:
                    if len(message.text) <= 40:
                        model_media["title"] = message.text
                        set_media_step(9)
                        await bot.send_message(
                            message.chat.id,
                            "Введите дедлайн задачи в формате\n"
                            "ГОД-МЕСЯЦ-ЧИСЛО ЧАСЫ:МИНУТЫ\nНапример 2023-02-24 04:00",
                            reply_markup=choice_media_type_date()
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

                        desc_card = f"Валюта : {model_media['currency_type']}\n" \
                                    f"Гео : {model_media['geo']}\n" \
                                    f"Тайминг видео : {model_media['timing_video']}\n" \
                                    f"Формат креатива : {model_media['format']}\n" \
                                    f"Количество креативов : {model_media['count']}\n" \
                                    f"Оффер : {model_media['offer']}\n\n" \
                                    f"Вложения для ТЗ : \n{model_media['source']}\n\n" \
                                    f"Описание доп : \n{model_media['desc']}\n\n" \
                                    f"Связь в тг: @{message.chat.username}\n"

                        current_user = get_user(message.chat.id)
                        result_add_to_db = add_card(model_media['title'], desc_card, "cards_creo").result

                        if result_add_to_db is not None:
                            create_card_creo(
                                TrelloCard(
                                    name=f"#{result_add_to_db['id']} Заказать Креатив ({model_media['title']})",
                                    desc=desc_card
                                ),
                                owner_dep=current_user.result.dep_user,
                                owner_name=current_user.result.label_creo,
                                date=dateTime
                            )
                            await bot.send_message(message.chat.id, "Задание отправленно!",
                                                   reply_markup=setStartButton())

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
        await bot.send_message(message.chat.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: True)
async def answer(call):
    global user_state
    set_state_none()  # reset user state

    if get_user(call.from_user.id).result is not None:
        match call.data:
            case "edit_offer":
                user_state = "edit_offer"
                reset_offer()
                set_offer_step(0)
                model_offer["operation"] = "Редактировать оффер"
                await bot.send_message(
                    call.from_user.id,
                    "Id оффера в трекере : ",
                    reply_markup=close_markup
                )
            case "add_offer":
                user_state = "add_offer"
                reset_offer()
                set_offer_step(0)

                await bot.send_message(
                    call.from_user.id,
                    "Новый рекламодатель или существующий?",
                    reply_markup=choice_offer_type()
                )
            case "order_creative":
                user_state = "order_creative"
                reset_media()
                set_media_step(0)

                await bot.send_message(
                    call.from_user.id,
                    "Язык, валюта: (например: CAD/или символ валюты) : ",
                    reply_markup=close_markup
                )
    else:
        await bot.send_message(call.from_user.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
