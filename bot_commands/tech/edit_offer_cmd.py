import datetime

from bot_commands.state_managment import set_state_none
from bot_helper.main_tasks import set_start_button
from db_helper.db_manager import get_user_db, add_card_db, update_card_db
from messages.const_messages import MESSAGE_SEND, MESSAGE_DONT_SEND
from models.task_form import task_step, model_task_list, set_task_step
from trello_helper.trello_manager import create_card_tech, TrelloCard, card_labels_tech


async def edit_offer_cmd(message, bot):
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

            current_user = get_user_db(message.chat.id)
            result_add_to_db = add_card_db(
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
