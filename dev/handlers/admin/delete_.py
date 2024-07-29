from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard, menu_keyboard
from constants.base import INPUT_USER_ID, NOT_ACCESS, USER_HAVE_NOT_IN_DB, ERROR_DELETE_USER, USER_DELETED
from constants.dep import ADMIN_
from handlers.admin.states_admin.admin_states import StateDeleteUser
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def delte_admin_handlers(dispatcher):
    dispatcher.register_message_handler(delete_user, commands=['delete_user'])
    dispatcher.register_message_handler(delete_user_cmd, state=StateDeleteUser.delete_user)


async def delete_user(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep == ADMIN_:
        await StateDeleteUser.delete_user.set()
        await message.answer(INPUT_USER_ID, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def delete_user_cmd(message: types.Message, state: FSMContext):
    if UserRepository().get_user(message.text) is not None:
        if UserRepository().delete_user(message.text) is not None:
            await state.finish()
            await message.answer(USER_DELETED, reply_markup=menu_keyboard())
        else:
            await message.answer(ERROR_DELETE_USER)
    else:
        await message.answer(USER_HAVE_NOT_IN_DB)
