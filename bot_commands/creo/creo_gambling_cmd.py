import datetime

from bot_commands.state_managment import set_state_none
from bot_helper.creo_tasks import plash_google_apple
from bot_helper.main_tasks import skip_desc, close_markup, yes_no, choice_date, set_start_button
from db_helper.db_manager import get_user_db, add_card_db, update_card_db
from messages.const_messages import SKIP, TIME_CHOICE, MESSAGE_SEND, MESSAGE_DONT_SEND, WRONG_TIME_CHOICE, \
    ERROR_OPERATION
from models.task_form import task_step, model_task_list, set_task_step
from trello_helper.trello_manager import create_card_creo, TrelloCard, add_attachments_to_card, card_labels_creo, \
    id_creo_gambling


async def order_gambling_creative(message, bot):
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
            model_task_list["emotions"] = message.text
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
            model_task_list["sms"] = message.text
            set_task_step(9)
            await bot.send_message(
                message.chat.id,
                "Телефон із повідомленням (Так, Ні) : ",
                reply_markup=yes_no()
            )
        case 9:
            model_task_list["phone_notify"] = message.text
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
                "Вкладення для ТЗ: посилання на картинки/відео через кому "
                "Наприклад: \nhttps://google.com/,https://google.com/",
                reply_markup=skip_desc()
            )
        case 13:
            try:
                model_task_list["reference"] = [] if message.text == SKIP else message.text.split(",")
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
                    date_time = datetime.datetime.strptime(
                        datetime.datetime.now().strftime("%Y-%m-%d") +
                        " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                + datetime.timedelta(days=1)
                elif message.text == SKIP:
                    date_time = ""
                else:
                    date_time = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

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

                current_user = get_user_db(message.chat.id)
                result_add_to_db = add_card_db(
                    f"Order Gambling Creative by ({current_user.result.name_user})",
                    f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                    "cards_creo",
                    message.chat.id,
                ).result

                if result_add_to_db is not None:
                    card = card_id = create_card_creo(
                        TrelloCard(
                            name=f"#{result_add_to_db['id']} Креатив Gambling ({model_task_list['type_creo']})",
                            desc=desc_card
                        ),
                        labels=[current_user.result.label_creo, card_labels_creo[current_user.result.dep_user]],
                        date=date_time,
                        list_creo=id_creo_gambling
                    )
                    update_card_db(result_add_to_db['id'], card.json()['id'], "cards_creo")

                    add_attachments_to_card(
                        card_id=card_id.json()['id'],
                        source=model_task_list['reference']
                    )

                    if card_id.ok:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_SEND,
                            reply_markup=set_start_button()
                        )
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=set_start_button()
                        )

                    set_state_none()  # reset user state
                else:
                    await bot.send_message(
                        message.chat.id,
                        MESSAGE_DONT_SEND,
                        reply_markup=set_start_button()
                    )
                    set_state_none()  # reset user state
            except Exception as e:
                print(e)
                if str(e).__contains__("does not match format '%Y-%m-%d %H:%M %z'"):
                    await bot.reply_to(message, WRONG_TIME_CHOICE)
                else:
                    set_state_none()  # reset user state
                    await bot.reply_to(message, ERROR_OPERATION)


async def order_gambling_creative_adaptive(message, bot):
    match task_step["step"]:
        case 0:
            try:
                model_task_list["amount_creo"] = int(message.text)
                set_task_step(1)
                await bot.send_message(message.chat.id, "Гео,мова : ")
            except Exception as e:
                await bot.send_message(message.chat.id, "Введіть число : ")
                print(f"order gambling creo (input count of creo) {e}")
        case 1:
            model_task_list["geo_lang"] = message.text
            set_task_step(2)
            await bot.send_message(message.chat.id, "Опис ТЗ (Детально) : ")
        case 2:
            model_task_list["desc"] = message.text
            set_task_step(3)
            await bot.send_message(
                message.chat.id,
                "Вкладення для ТЗ: посилання на картинки/відео через кому "
                "Наприклад: \nhttps://google.com/,https://google.com/",
                reply_markup=skip_desc()
            )
        case 3:
            try:
                model_task_list["link_source"] = [] if message.text == SKIP else message.text.split(",")
                set_task_step(4)
                await bot.send_message(
                    message.chat.id,
                    TIME_CHOICE,
                    reply_markup=choice_date()
                )
            except Exception as e:
                await bot.send_message(message.chat.id, "Спробуйте ще раз (формат через кому) : ")
                print(e)
        case 4:
            try:
                if message.text in ("Завтра 12:00", "Завтра 15:00", "Завтра 18:00"):
                    date_time = datetime.datetime.strptime(
                        datetime.datetime.now().strftime("%Y-%m-%d") +
                        " " + message.text.split(" ")[1] + " +0300", '%Y-%m-%d %H:%M %z') \
                                + datetime.timedelta(days=1)
                elif message.text == SKIP:
                    date_time = ""
                else:
                    date_time = datetime.datetime.strptime(message.text + " +0300", '%Y-%m-%d %H:%M %z')

                desc_card = f"Тип : {model_task_list['type_creo']}\n" \
                            f"Кількість : {model_task_list['amount_creo']}\n" \
                            f"Гео,мова : {model_task_list['geo_lang']}\n\n" \
                            f"Опис ТЗ : {model_task_list['desc']}\n\n" \
                            f"Зв'язок у тг: @{message.chat.username}\n"

                current_user = get_user_db(message.chat.id)
                result_add_to_db = add_card_db(
                    f"Order Gambling Creative by ({current_user.result.name_user})",
                    f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                    "cards_creo",
                    message.chat.id,
                ).result

                if result_add_to_db is not None:
                    card = card_id = create_card_creo(
                        TrelloCard(
                            name=f"#{result_add_to_db['id']} Креатив Gambling ({model_task_list['type_creo']})",
                            desc=desc_card
                        ),
                        labels=[current_user.result.label_creo, card_labels_creo[current_user.result.dep_user]],
                        date=date_time,
                        list_creo=id_creo_gambling
                    )
                    update_card_db(result_add_to_db['id'], card.json()['id'], "cards_creo")

                    add_attachments_to_card(
                        card_id=card_id.json()['id'],
                        source=model_task_list['link_source']
                    )

                    if card_id.ok:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_SEND,
                            reply_markup=set_start_button()
                        )
                    else:
                        await bot.send_message(
                            message.chat.id,
                            MESSAGE_DONT_SEND,
                            reply_markup=set_start_button()
                        )

                    set_state_none()  # reset user state
                else:
                    await bot.send_message(
                        message.chat.id,
                        MESSAGE_DONT_SEND,
                        reply_markup=set_start_button()
                    )
                    set_state_none()  # reset user state

            except Exception as e:
                print(e)
                if str(e).__contains__("does not match format '%Y-%m-%d %H:%M %z'"):
                    await bot.reply_to(message, WRONG_TIME_CHOICE)
                else:
                    set_state_none()  # reset user state
                    await bot.reply_to(message, ERROR_OPERATION)
