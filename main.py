from telebot import types

from config import DEBUG_MODE
from db_helper.db_manager import add_user, User, delete_user, get_user, get_list_users, add_card
from bot_helper.menu_buttons import setStartButton, af_manager_menu, choice_offer_type
from models.af_manager_model import model_offer, offer_step, set_offer_step, reset_offer
from private_config import local_telegram_token, server_telegram_token
from telebot.async_telebot import AsyncTeleBot
import asyncio

from trello_helper.trello_manager import create_card_tech, TrelloCard, create_label

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
}

user_state = "none"

# dep states
dep_states = {"admin", "gamble_ppc", "gamble_uac", "gamble_fb", "af_manager", "the_PR"}

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
async def user_delete_add(message):
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


@bot.message_handler(func=lambda m: m.text in ("Gambling FB", "Gambling PPC", "Gambling UAC", "AF Manager", "Schema"))
async def choice_category(message):
    set_state_none()  # reset user state

    if get_user(message.chat.id).result is not None:
        match message.text:
            case "AF Manager":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=af_manager_menu())
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
    else:
        await bot.send_message(call.from_user.id, 'Вы не зарегестрированы, напишите админу', reply_markup=close_markup)


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
