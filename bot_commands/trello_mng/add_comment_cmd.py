from bot_commands.state_managment import set_state_none
from bot_helper.main_tasks import set_start_button
from models.task_form import model_task_list
from trello_helper.trello_manager import write_comment


async def add_comment_cmd(message, bot):
    try:
        if write_comment(id_card=model_task_list["current_card"], text=message.text):
            await bot.send_message(
                message.chat.id,
                "✅ Коментар доданий",
                reply_markup=set_start_button()
            )
        else:
            await bot.send_message(
                message.chat.id,
                "Помилка при додаванні коментарю",
                reply_markup=set_start_button()
            )
    except:
        pass
    set_state_none()  # reset user state
