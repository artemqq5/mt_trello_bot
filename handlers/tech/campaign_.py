from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import cancel_keyboard
from _keyboard.tech_keyboard.tech_keyboard import tech_choice
from constants.base import NOT_ACCESS
from constants.tech import *
from handlers.tech.state_tech.tech_states import StateTechTask, StateCreateCampaign
from handlers.tech.tools.send_task import send_order_tech
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model


def register_create_campaign_tech_handler(dispatcher):
    dispatcher.register_message_handler(start_create_campaign, lambda m: m.text == CREATE_CAMPAIGN,
                                        state=StateTechTask.set_task)

    dispatcher.register_message_handler(set_geo_campaign, state=StateCreateCampaign.geo)
    dispatcher.register_message_handler(set_app_name_campaign, state=StateCreateCampaign.app_name)


async def start_create_campaign(message: types.Message):
    if get_user_model(UserRepository().get_user(message.chat.id)).dep in CREATE_CAMPAIGN_ACCESS:
        await StateCreateCampaign.geo.set()
        await message.answer(INPUT_GEO, reply_markup=cancel_keyboard())
    else:
        await message.answer(NOT_ACCESS)


async def set_geo_campaign(message: types.Message, state: FSMContext):
    await state.update_data(geo=message.text)
    await StateCreateCampaign.app_name.set()
    await message.answer(INPUT_APP_NAME)


async def set_app_name_campaign(message: types.Message, state: FSMContext):
    await state.update_data(app_name=message.text)
    await state.update_data(type_task=CREATE_CAMPAIGN)

    await state.set_state(StateTechTask.choice_tech)
    await message.answer(CHOICE_TECH, reply_markup=tech_choice)

