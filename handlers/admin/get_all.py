from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import dep_keyboard
from constants.base import CHOICE_DEP_USER, NOT_ACCESS, ERROR_OPERATION, ALL_DEP, LIST_IS_EMPTY
from constants.dep import ADMIN_, DEP_LIST
from handlers.admin.states_admin.admin_states import StateGetAllUsers
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model, get_user_model_list


def get_all_admin_handlers(dispatcher):
    dispatcher.register_message_handler(get_all, commands=['get_all'])
    dispatcher.register_message_handler(get_all_cmd, lambda m: m.text in DEP_LIST + (ALL_DEP,),
                                        state=StateGetAllUsers.get_all_users)


async def get_all(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep == ADMIN_:
        await StateGetAllUsers.get_all_users.set()
        await message.answer(CHOICE_DEP_USER, reply_markup=dep_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def get_all_cmd(message: types.Message, state: FSMContext):
    forrmated = ""

    # get all users if MESSAGE.TEXT == "Всі користувачі" else get users by dep
    users = get_user_model_list(UserRepository().get_users()) if message.text == ALL_DEP else get_user_model_list(
        UserRepository().get_users_by_dep(message.text))

    if users is not None:
        for user in users:
            dep = f"<b>Dep:</b> {user.dep}\n\n" if message.text == ALL_DEP else "\n"
            forrmated += f"<b>ID:</b> {user.id}\n<b>Name:</b> {user.name}\n{dep}"
        await message.answer(forrmated)
    else:
        await message.answer(LIST_IS_EMPTY)

    await state.finish()
