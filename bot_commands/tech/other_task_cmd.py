import datetime

from bot_commands.state_managment import set_state_none
from bot_helper.main_tasks import set_start_button, choice_date
from db_helper.db_manager import get_user_db, add_card_db, update_card_db
from messages.const_messages import MESSAGE_SEND, MESSAGE_DONT_SEND, SKIP, TIME_CHOICE, WRONG_TIME_CHOICE
from models.task_form import task_step, model_task_list, set_task_step
from trello_helper.trello_manager import create_card_tech, TrelloCard, card_labels_tech


async def other_task_cmd(message, bot):
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
                    date_time = datetime.datetime.strptime(
                        datetime.datetime.now().strftime("%Y-%m-%d") +
                        " " + message.text.split(" ")[1] + " +0400", '%Y-%m-%d %H:%M %z') \
                                + datetime.timedelta(days=1)
                elif message.text == SKIP:
                    date_time = ""
                else:
                    date_time = datetime.datetime.strptime(message.text + " +0400", '%Y-%m-%d %H:%M %z')

                desc_card = f"{model_task_list['desc']}\n\n" \
                            f"Зв'язок у тг: @{message.chat.username}\n"

                current_user = get_user_db(message.chat.id)
                result_add_to_db = add_card_db(
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
                        labels=[current_user.result.label_tech, card_labels_tech[current_user.result.dep_user]],
                        date=date_time
                    )
                    update_card_db(result_add_to_db['id'], card.json()['id'], "cards_tech")
                    await bot.send_message(message.chat.id, MESSAGE_SEND,
                                           reply_markup=set_start_button())
                else:
                    await bot.send_message(
                        message.chat.id,
                        MESSAGE_DONT_SEND,
                        reply_markup=set_start_button()
                    )

                set_state_none()  # reset user state
            except Exception as e:
                print(e)
                await bot.reply_to(
                    message,
                    WRONG_TIME_CHOICE
                )
