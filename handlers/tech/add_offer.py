from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard
from _keyboard.tech_keyboard.tech_keyboard import tech_advertiser_type_keyboard, tech_choice
from constants.base import NOT_ACCESS
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateAddOffer
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_add_offer_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_add_offer, lambda m: m.text == ADD_OFFER, state=StateTechTask.set_task)
    dispatcher.register_message_handler(set_advertiser_type, lambda m: m.text in (TYPE_TECH_NEW, TYPE_TECH_EXIST),
                                        state=StateAddOffer.advertiser_type)
    dispatcher.register_message_handler(set_telegram_group, state=StateAddOffer.tg_group)
    dispatcher.register_message_handler(set_advertiser_name, state=StateAddOffer.advertiser_name)
    dispatcher.register_message_handler(set_name_offer, state=StateAddOffer.offer_name)
    dispatcher.register_message_handler(set_geo_offer, state=StateAddOffer.geo)
    dispatcher.register_message_handler(set_geo_deduction_offer, state=StateAddOffer.geo_deduction)
    dispatcher.register_message_handler(set_promo_link, state=StateAddOffer.promo_link)


async def start_add_offer(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in ADD_OFFER_ACCESS:
        await StateAddOffer.advertiser_type.set()
        await message.answer(INPUT_TYPE_ADVERTISER, reply_markup=tech_advertiser_type_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_advertiser_type(message: types.Message, state: FSMContext):
    await state.update_data(advertiser_type=message.text)

    if message.text == TYPE_TECH_NEW:
        await StateAddOffer.tg_group.set()
        await message.answer(INPUT_TELEGRAM_GROUP, reply_markup=cancel_keyboard())
    else:
        await StateAddOffer.advertiser_name.set()
        await message.answer(INPUT_ADVERTISER_NAME, reply_markup=cancel_keyboard())


async def set_telegram_group(message: types.Message, state: FSMContext):
    await StateAddOffer.advertiser_name.set()
    await state.update_data(telegram_group=message.text)
    await message.answer(INPUT_ADVERTISER_NAME)


async def set_advertiser_name(message: types.Message, state: FSMContext):
    await StateAddOffer.offer_name.set()
    await state.update_data(advertiser_name=message.text)
    await message.answer(INPUT_OFFER_NAME)


async def set_name_offer(message: types.Message, state: FSMContext):
    await StateAddOffer.geo.set()
    await state.update_data(offer_name=message.text)
    await message.answer(INPUT_GEO)


async def set_geo_offer(message: types.Message, state: FSMContext):
    await StateAddOffer.geo_deduction.set()
    await state.update_data(geo=message.text)
    await message.answer(INPUT_GEO_DEDUCATION)


async def set_geo_deduction_offer(message: types.Message, state: FSMContext):
    await StateAddOffer.promo_link.set()
    await state.update_data(geo_deduction=message.text)
    await message.answer(INPUT_PROMO_LINK)


async def set_promo_link(message: types.Message, state: FSMContext):
    await state.update_data(promo_link=message.text)
    await state.update_data(type_task=ADD_OFFER)

    await state.set_state(StateTechTask.choice_tech)
    await message.answer(CHOICE_TECH, reply_markup=tech_choice)




