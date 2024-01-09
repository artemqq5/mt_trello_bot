from aiogram import types
from aiogram.dispatcher import FSMContext
from trello import TrelloClient

from _keyboard.base_keyboard import cancel_keyboard, menu_keyboard
from constants.base import INPUT_USER_ADD, NOT_ACCESS, INPUT_USER_ADD_ERROR, HAVE_NOT_DEP, USER_ALREADY_HAVE, \
    USER_ADD_ERROR, USER_ADDED
from constants.dep import ADMIN_, DEP_LIST
from handlers.admin.states_admin.admin_states import StateAddUser
from repository.model.user import UserModel
from repository.trello_.trello_repository import TrelloRepository
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def add_admin_handlers(dispatcher):
    dispatcher.register_message_handler(add_user, commands=['add_user'])
    dispatcher.register_message_handler(add_user_cmd, state=StateAddUser.add_user)


async def add_user(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep == ADMIN_:
        await StateAddUser.add_user.set()
        await message.answer(INPUT_USER_ADD, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def add_user_cmd(message: types.Message, state: FSMContext):
    data_user = message.text.split(" ")
    if len(data_user) == 3:
        if data_user[2] in DEP_LIST:
            if UserRepository().get_user(data_user[0]) is None:
                user = UserModel(id_user=data_user[0], name_user=data_user[1], dep_user=data_user[2],
                                 label_creo=TrelloRepository().create_label_creo(data_user[1]),
                                 label_tech=TrelloRepository().create_label_creo(data_user[1]))

                if UserRepository().add_user(user) is not None:
                    await state.finish()
                    await message.answer(USER_ADDED, reply_markup=menu_keyboard())
                else:
                    await message.answer(USER_ADD_ERROR)
            else:
                await message.answer(USER_ALREADY_HAVE)
        else:
            await message.answer(f'{HAVE_NOT_DEP} {DEP_LIST} :')
    else:
        await message.answer(INPUT_USER_ADD_ERROR)
