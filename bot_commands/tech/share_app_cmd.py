import datetime

from bot_commands.state_managment import set_state_none
from bot_helper.main_tasks import set_start_button, skip_desc
from db_helper.db_manager import get_user_db, add_card_db, update_card_db
from messages.const_messages import MESSAGE_SEND, MESSAGE_DONT_SEND, SKIP
from models.task_form import task_step, model_task_list, set_task_step
from trello_helper.trello_manager import create_card_tech, TrelloCard, card_labels_tech


async def share_app_cmd(message, bot):
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

            current_user = get_user_db(message.chat.id)
            result_add_to_db = add_card_db(
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
                    labels=[current_user.result.label_tech, card_labels_tech[current_user.result.dep_user]],
                )
                update_card_db(result_add_to_db['id'], card.json()['id'], "cards_tech")
                await bot.send_message(message.chat.id, MESSAGE_SEND, reply_markup=set_start_button())
            else:
                await bot.send_message(
                    message.chat.id,
                    MESSAGE_DONT_SEND,
                    reply_markup=set_start_button()
                )


