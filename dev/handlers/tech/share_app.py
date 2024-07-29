from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard
from _keyboard.tech_keyboard.tech_keyboard import tech_choice
from constants.base import NOT_ACCESS
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateShareApp
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_share_app_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_share_app, lambda m: m.text == SHARE_APP, state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_name_share, state=StateShareApp.name)
    dispatcher.register_message_handler(set_id_cabinets_share, state=StateShareApp.id_cabinets)
    dispatcher.register_message_handler(set_desc_share, state=StateShareApp.desc)


async def start_share_app(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in SHARE_APP_ACCESS:
        await StateShareApp.name.set()
        await message.answer(INPUT_APP_NAME, reply_markup=(cancel_keyboard()))
    else:
        await message.answer(NOT_ACCESS)


async def set_name_share(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await StateShareApp.id_cabinets.set()
    await message.answer(INPUT_ID_CABINETS)


async def set_id_cabinets_share(message: types.Message, state: FSMContext):
    await state.update_data(id_cabinets=message.text)
    await StateShareApp.desc.set()
    await message.answer(INPUT_DESC)


async def set_desc_share(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.update_data(type_task=SHARE_APP)

    await state.set_state(StateTechTask.choice_tech)
    await message.answer(CHOICE_TECH, reply_markup=tech_choice)
