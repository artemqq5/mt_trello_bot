from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard
from constants.base import NOT_ACCESS
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateSettingCloak
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_cloak_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_setting_cloak, lambda m: m.text == SETTING_CLOAK,
                                        state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_geo_cloak, state=StateSettingCloak.geo)
    dispatcher.register_message_handler(set_offer_cloak, state=StateSettingCloak.offer)
    dispatcher.register_message_handler(set_domains_cloak, state=StateSettingCloak.domains)
    dispatcher.register_message_handler(set_desc_cloak, state=StateSettingCloak.desc)


async def start_setting_cloak(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in SETTING_CLOAK_ACCESS:
        await StateSettingCloak.geo.set()
        await message.answer(INPUT_GEO, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_geo_cloak(message: types.Message, state: FSMContext):
    await state.update_data(geo=message.text)
    await StateSettingCloak.offer.set()
    await message.answer(INPUT_OFFER)


async def set_offer_cloak(message: types.Message, state: FSMContext):
    await state.update_data(offer=message.text)
    await StateSettingCloak.domains.set()
    await message.answer(INPUT_DOMAINS)


async def set_domains_cloak(message: types.Message, state: FSMContext):
    await state.update_data(domains=message.text)
    await StateSettingCloak.desc.set()
    await message.answer(INPUT_DESC)


async def set_desc_cloak(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    await state.finish()
    await send_order_tech(data=data, message=message, type_=SETTING_CLOAK)
