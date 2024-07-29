from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard
from _keyboard.my_task.my_task_keyboard import my_task_creo_callback_keyboard, my_task_tech_callback_keyboard, \
    manage_task_keyboard, choose_tasks_keyboard
from constants.my_task import *
from handlers.my_task.state_my_task.my_task_states import StateMyTaskManage
from handlers.my_task.tools.message_tools import info_about_card
from repository.trello_.trello_repository import TrelloRepository
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_my_task_handler(dispatcher):
    dispatcher.register_message_handler(start_handle_task, lambda m: m.text in (MY_CREO_TASK, MY_TECH_TASK),
                                        state=StateMyTaskManage.start_manage)
    dispatcher.register_message_handler(set_comment_card, state=StateMyTaskManage.comment)

    dispatcher.register_callback_query_handler(managment_cards_callback, state=StateMyTaskManage.start_manage)


async def start_handle_task(message: types.Message, state: FSMContext):
    user = get_user_model(UserRepository().get_user(message.chat.id))

    await message.answer(LOADING_TASK)

    if message.text == MY_CREO_TASK:
        await message.answer(MY_CREO_TASK, reply_markup=my_task_creo_callback_keyboard(user))
    else:
        await message.answer(MY_TECH_TASK, reply_markup=my_task_tech_callback_keyboard(user))


async def set_comment_card(message: types.Message, state: FSMContext):
    user_message = message.text
    data = await state.get_data()
    result = TrelloRepository().write_comment(data['id_card'], user_message)
    await StateMyTaskManage.start_manage.set()
    if result is not None:
        await message.answer(COMMENT_SUCCESS_SENDED, reply_markup=choose_tasks_keyboard())
    else:
        await message.answer(COMMENT_FAIL_SENDED, reply_markup=choose_tasks_keyboard())


async def managment_cards_callback(callback: types.CallbackQuery, state: FSMContext):
    mode = callback.data.split("_")[0]
    id_card = callback.data.split("_")[1]

    try:
        if mode == "card":
            await callback.message.answer(info_about_card(id_card), reply_markup=manage_task_keyboard(id_card))
        elif mode == "comment":
            await StateMyTaskManage.comment.set()
            await state.update_data(id_card=id_card)
            await callback.message.answer(INPUT_COMMENT, reply_markup=cancel_keyboard())
        elif mode == "delete":
            result = TrelloRepository().delete_card(id_card)
            if result is not None:
                await callback.message.answer(TASK_SUCCESS_DELETED, reply_markup=choose_tasks_keyboard())
            else:
                await callback.message.answer(TASK_FAIL_DELETED, reply_markup=choose_tasks_keyboard())
    except Exception as e:
        print(f"managment_cards_callback error: {e}")
