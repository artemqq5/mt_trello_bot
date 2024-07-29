import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard, skip_keyboard
from _keyboard.tech_keyboard.tech_keyboard import tech_choice
from constants.base import NOT_ACCESS, SKIP, WRONG_TIME_CHOICE, DEADLINE_MESSAGE
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateCreatePWA
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_pwa_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_create_pwa, lambda m: m.text == PWA_, state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_geo_pwa, state=StateCreatePWA.geo)
    dispatcher.register_message_handler(set_name_pwa, state=StateCreatePWA.name)
    dispatcher.register_message_handler(set_desc_pwa, state=StateCreatePWA.desc)
    dispatcher.register_message_handler(set_deadline_pwa, state=StateCreatePWA.deadline)


async def start_create_pwa(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in PWA_ACCESS:
        await StateCreatePWA.geo.set()
        await message.answer(INPUT_GEO, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_geo_pwa(message: types.Message, state: FSMContext):
    await state.update_data(geo=message.text)
    await StateCreatePWA.name.set()
    await message.answer(INPUT_APP_NAME)


async def set_name_pwa(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await StateCreatePWA.desc.set()
    await message.answer(INPUT_DESC)


async def set_desc_pwa(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await StateCreatePWA.deadline.set()
    await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())


async def set_deadline_pwa(message: types.Message, state: FSMContext):
    if message.text != SKIP:
        try:
            date_time = datetime.datetime.strptime(message.text + " +0400", '%Y-%m-%d %H:%M %z')

            await state.update_data(deadline=str(date_time))
            await state.update_data(type_task=PWA_)

            await state.set_state(StateTechTask.choice_tech)
            await message.answer(CHOICE_TECH, reply_markup=tech_choice)
        except Exception as e:
            print(f"set_deadline_pwa - {e}")
            await message.answer(WRONG_TIME_CHOICE, reply_markup=skip_keyboard())

    else:
        await state.update_data(deadline=None)
        await state.update_data(type_task=PWA_)

        await state.set_state(StateTechTask.choice_tech)
        await message.answer(CHOICE_TECH, reply_markup=tech_choice)
