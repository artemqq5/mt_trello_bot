import datetime

from bot_commands.state_managment import set_state_none
from bot_helper.creo_categories.media_other import choice_source_media, account_or_app_media
from bot_helper.main_tasks import skip_desc, close_markup, choice_date, set_start_button
from db_helper.db_manager import get_user_db, add_card_db, update_card_db
from messages.const_messages import SKIP, TIME_CHOICE, MESSAGE_SEND, MESSAGE_DONT_SEND, WRONG_TIME_CHOICE, \
    ERROR_OPERATION
from models.task_form import task_step, model_task_list, set_task_step
from trello_helper.trello_manager import create_card_creo, TrelloCard, card_labels_creo, id_creo_media


async def order_media_creative(message, bot):
    match task_step["step"]:
        case 0:
            try:
                model_task_list["amount_creo"] = int(message.text)
                set_task_step(1)
                await bot.send_message(
                    message.chat.id,
                    "Розмір у пікселях або роздільна здатність (1к1 або 1080 на 1080) : ")
            except Exception as e:
                await bot.send_message(message.chat.id, "Введіть число : ")
                print(f"order media creo (input count of creo) {e}")
        case 1:
            model_task_list["px_size"] = message.text
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

                desc_card = f"Кількість : {model_task_list['amount_creo']}\n" \
                            f"Розмір у пікселях або роздільна здатність : {model_task_list['px_size']}\n\n" \
                            f"Опис : \n{model_task_list['desc']}\n\n" \
                            f"Зв'язок у тг: @{message.chat.username}\n"

                current_user = get_user_db(message.chat.id)
                result_add_to_db = add_card_db(
                    f"Order Media Creative by ({current_user.result.name_user})",
                    f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}",
                    "cards_creo",
                    message.chat.id,
                ).result

                if result_add_to_db is not None:
                    card = card_id = create_card_creo(
                        TrelloCard(
                            name=f"#{result_add_to_db['id']} Креатив Media&Other ({model_task_list['type_creo']})",
                            desc=desc_card
                        ),
                        labels=[current_user.result.label_creo, card_labels_creo[current_user.result.dep_user]],
                        date=date_time,
                        list_creo=id_creo_media
                    )
                    update_card_db(result_add_to_db['id'], card.json()['id'], "cards_creo")

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
