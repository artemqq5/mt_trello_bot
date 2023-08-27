import datetime

from bot_commands.state_managment import set_state_none
from bot_helper.main_tasks import close_markup, set_start_button
from db_helper.db_manager import get_user_db, add_card_db, update_card_db
from messages.const_messages import MESSAGE_SEND, MESSAGE_DONT_SEND
from models.task_form import task_step, model_task_list, set_task_step
from trello_helper.trello_manager import create_card_tech, TrelloCard, card_labels_tech


async def add_offer_cmd(message, bot):
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

            current_user = get_user_db(message.chat.id)
            result_add_to_db = add_card_db(
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
