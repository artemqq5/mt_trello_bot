from constants.creo import DESIGN
from constants.dep import DESIGNER_
from repository.card_repository.card_repos import CardRepository
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model_list


async def notify_new_creo(message, trellocard, url):
    users = get_user_model_list(UserRepository().get_users())

    info_task = f"<b>{trellocard.name}</b>\n\n"
    info_task += f"{trellocard.desc}\n"
    info_task += f"{url}"

    try:
        for user in users:
            if user.dep == DESIGNER_:
                await message.bot.send_message(chat_id=user.id, text=info_task)
    except Exception as e:
        print(f"notify_new_creo: {e}")

