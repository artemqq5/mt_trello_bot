from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard
from constants.base import NOT_ACCESS
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateEditOffer
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_edit_offer_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_edit_offer, lambda m: m.text == EDIT_OFFER,
                                        state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_offer_id, state=StateEditOffer.offer_id)
    dispatcher.register_message_handler(set_offer_desc, state=StateEditOffer.desc)


async def start_edit_offer(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in EDIT_OFFER_ACCESS:
        await StateEditOffer.offer_id.set()
        await message.answer(INPUT_OFFER_ID, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_offer_id(message: types.Message, state: FSMContext):
    await state.update_data(offer_id=message.text)
    await StateEditOffer.desc.set()
    await message.answer(INPUT_DESC)


async def set_offer_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    await state.finish()
    await send_order_tech(data=data, message=message, type_=EDIT_OFFER)

