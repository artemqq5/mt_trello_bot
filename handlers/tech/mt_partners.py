import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard, skip_keyboard
from constants.base import NOT_ACCESS, SKIP, WRONG_TIME_CHOICE, DEADLINE_MESSAGE
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateMTPartners
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_mt_partners_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_mt_partners, lambda m: m.text == TASK_MT_PARTNERS,
                                        state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_desc_mt_partners, state=StateMTPartners.desc)
    dispatcher.register_message_handler(set_deadline_mt_partners, state=StateMTPartners.deadline)


async def start_mt_partners(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in MT_PARTNERS_ACCESS:
        await StateMTPartners.desc.set()
        await message.answer(INPUT_DESC, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_desc_mt_partners(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await StateMTPartners.deadline.set()
    await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())


async def set_deadline_mt_partners(message: types.Message, state: FSMContext):
    if message.text != SKIP:
        try:
            date_time = datetime.datetime.strptime(message.text + " +0400", '%Y-%m-%d %H:%M %z')

            await state.update_data(deadline=str(date_time))
            data = await state.get_data()
            await state.finish()

            await send_order_tech(data=data, message=message, type_=TASK_MT_PARTNERS)
        except Exception as e:
            print(f"set_deadline_mt_partners - {e}")
            await message.answer(WRONG_TIME_CHOICE, reply_markup=skip_keyboard())

    else:
        await state.update_data(deadline=None)
        data = await state.get_data()
        await state.finish()
        await send_order_tech(data=data, message=message, type_=TASK_MT_PARTNERS)

