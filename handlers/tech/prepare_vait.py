import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard, skip_keyboard
from constants.base import NOT_ACCESS, SKIP, WRONG_TIME_CHOICE
from constants.creo import DEADLINE_MESSAGE
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StatePrepareVait
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_prepare_vait_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_prepare_vait, lambda m: m.text == PREPARE_VAIT,
                                        state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_geo_vait, state=StatePrepareVait.geo)
    dispatcher.register_message_handler(set_source_vait, state=StatePrepareVait.source)
    dispatcher.register_message_handler(set_technical_task_vait, state=StatePrepareVait.technical_task_link)
    dispatcher.register_message_handler(set_desc_vait, state=StatePrepareVait.desc)
    dispatcher.register_message_handler(set_deadline_vait, state=StatePrepareVait.deadline)


async def start_prepare_vait(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in OTHER_TECH_ACCESS:
        await StatePrepareVait.geo.set()
        await message.answer(INPUT_GEO, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_geo_vait(message: types.Message, state: FSMContext):
    await state.update_data(geo=message.text)
    await StatePrepareVait.source.set()
    await message.answer(INPUT_SOURCE)


async def set_source_vait(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)
    await StatePrepareVait.technical_task_link.set()
    await message.answer(INPUT_TECHNICAL_TASK)


async def set_technical_task_vait(message: types.Message, state: FSMContext):
    await state.update_data(technical_task=message.text)
    await StatePrepareVait.desc.set()
    await message.answer(INPUT_DESC)


async def set_desc_vait(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await StatePrepareVait.deadline.set()
    await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())


async def set_deadline_vait(message: types.Message, state: FSMContext):
    if message.text != SKIP:
        try:
            date_time = datetime.datetime.strptime(message.text + " +0400", '%Y-%m-%d %H:%M %z')

            await state.update_data(deadline=str(date_time))
            data = await state.get_data()
            await state.finish()
        except Exception as e:
            print(f"set_deadline_vait - {e}")
            data = None
            await message.answer(WRONG_TIME_CHOICE, reply_markup=skip_keyboard())

        await send_order_tech(data=data, message=message, type_=PREPARE_VAIT)

    else:
        await state.update_data(deadline=None)
        data = await state.get_data()
        await state.finish()

        await send_order_tech(data=data, message=message, type_=PREPARE_VAIT)
