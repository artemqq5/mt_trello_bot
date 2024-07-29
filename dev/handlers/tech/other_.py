import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard, skip_keyboard
from _keyboard.tech_keyboard.tech_keyboard import tech_choice
from constants.base import NOT_ACCESS, SKIP, WRONG_TIME_CHOICE, DEADLINE_MESSAGE
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateOtherTask
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_other_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_other_tech, lambda m: m.text == OTHER_TECH,
                                        state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_desc_other, state=StateOtherTask.desc)
    dispatcher.register_message_handler(set_deadline_other, state=StateOtherTask.deadline)


async def start_other_tech(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in OTHER_TECH_ACCESS:
        await StateOtherTask.desc.set()
        await message.answer(INPUT_DESC, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_desc_other(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await StateOtherTask.deadline.set()
    await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())


async def set_deadline_other(message: types.Message, state: FSMContext):
    if message.text != SKIP:
        try:
            date_time = datetime.datetime.strptime(message.text + " +0400", '%Y-%m-%d %H:%M %z')

            await state.update_data(deadline=str(date_time))
            await state.update_data(type_task=OTHER_TECH)

            await state.set_state(StateTechTask.choice_tech)
            await message.answer(CHOICE_TECH, reply_markup=tech_choice)
        except Exception as e:
            print(f"set_deadline_other - {e}")
            await message.answer(WRONG_TIME_CHOICE, reply_markup=skip_keyboard())
    else:
        await state.update_data(deadline=None)
        await state.update_data(type_task=OTHER_TECH)

        await state.set_state(StateTechTask.choice_tech)
        await message.answer(CHOICE_TECH, reply_markup=tech_choice)
