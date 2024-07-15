from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import menu_keyboard, cancel_keyboard
from constants.base import *
from constants.dep import ADMIN_
from handlers.admin.states_admin.admin_states import StateMailingAllUsers
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model, get_user_model_list


def mailing_all_admin_handlers(dispatcher):
    dispatcher.register_message_handler(mailing_all, commands=['mailing_all'])
    dispatcher.register_message_handler(mailing_all_cmd, state=StateMailingAllUsers.mailing_all_users)


async def mailing_all(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep == ADMIN_:
        await StateMailingAllUsers.mailing_all_users.set()
        await message.answer(MAIL_TO_ALL, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def mailing_all_cmd(message: types.Message, state: FSMContext):
    users = get_user_model_list(UserRepository().get_users())
    unsuccessful = 1
    user_error = ""

    for user in users:
        try:
            if user.id != str(message.chat.id):
                await message.bot.send_message(user.id, message.text)
        except Exception as e:
            print(f"mailing all error for user {user.id}: {e}")
            unsuccessful += 1
            user_error += f"{user.name} ({user.id})\n"

    await state.finish()
    await message.answer(
        f"📬 Успішно доставлено {len(users) - unsuccessful} користувачам з {len(users)-1}\n\n"
        f"Досі не зареєструвалися у боті: \n{user_error}",
        reply_markup=menu_keyboard()
    )
