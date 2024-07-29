from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.exceptions import MessageIsTooLong

from _keyboard.base_keyboard import cancel_keyboard, skip_keyboard
from _keyboard.creo_keyboard.creo_keyboard import design_type_keyboard, design_category_keyboard, \
    design_category_finance_keyboard, design_app_platform_keyboard, design_format_keyboard, check_task_view_keyboard
from constants.base import DEADLINE_MESSAGE, MESSAGE_IS_TOO_LONG
from constants.creo import *
from handlers.creo.state_creo.creo_states import StateOrderCreo, StateAppCreo, StateDefaultCreo, StateOtherCreo
from handlers.creo.tools.message_tools import check_view_order


def register_order_creo_handlers(dispatcher):
    dispatcher.register_message_handler(set_creo_format, lambda message: message.text in FORMAT_CREO_LIST,
                                        state=StateOrderCreo.format_creo)

    dispatcher.register_message_handler(set_creo_type, lambda message: message.text in TYPE_CREO_LIST,
                                        state=StateOrderCreo.type_creo)

    dispatcher.register_callback_query_handler(set_creo_category, lambda call: call.data in (
            CATEGORY_CREO_LIST_VIDEO + CATEGORY_CREO_LIST_STATIC + CATEGORY_CREO_LIST_GIF_ANIM + FINANCE_CATEGORY_LIST
    ), state=StateOrderCreo.category_creo)

    dispatcher.register_message_handler(check_order_task, lambda m: m.text in (ALL_TASK_GOOD, ORDER_AGAIN_RETURN),
                                        state=[StateAppCreo.check, StateDefaultCreo.check, StateOtherCreo.check])


# format -> creo_type
async def set_creo_format(message: types.Message, state: FSMContext):
    await state.update_data(format_creo=message.text)
    await StateOrderCreo.type_creo.set()
    await message.answer(DESIGN_TYPE, reply_markup=design_type_keyboard())


# type -> creo_category
async def set_creo_type(message: types.Message, state: FSMContext):
    await state.update_data(type_creo=message.text)
    await StateOrderCreo.category_creo.set()

    data = await state.get_data()
    keyboard_type = FORMAT_TO_CATEGORY[data['format_creo']]

    await message.answer(DESIGN_CATEGORY, reply_markup=design_category_keyboard(keyboard_type))


# category query handler ->
async def set_creo_category(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == FINANCE:  # send new keyboard to choice sub category
        await callback.message.answer(text=FINANCE, reply_markup=design_category_finance_keyboard())
    else:
        await state.update_data(category_creo=callback.data)
        start_data_order = await state.get_data()
        await state.finish()

        format_creo = start_data_order['format_creo']
        type_creo = start_data_order['type_creo']
        category_creo = start_data_order['category_creo']

        # APP Creo
        if category_creo == APP_DESIGN:
            await StateAppCreo.general.set()
            await state.update_data(general=start_data_order)
            await StateAppCreo.platform.set()

            await callback.message.answer(PLATFORM_MESSAGE, reply_markup=design_app_platform_keyboard())

        # Custom Creo (Other)
        elif category_creo == OTHER:
            await StateOtherCreo.general.set()
            await state.update_data(general=start_data_order)
            await StateOtherCreo.format.set()

            if type_creo == NEW_CREATIVE:
                await callback.message.answer(FORMAT_MESSAGE, reply_markup=cancel_keyboard())
            else:
                await callback.message.answer(FORMAT_MESSAGE, reply_markup=skip_keyboard())

        # all default categories of Creo
        else:
            await StateDefaultCreo.general.set()
            await state.update_data(general=start_data_order)
            await StateDefaultCreo.geo.set()

            if type_creo == NEW_CREATIVE:
                await callback.message.answer(GEO_MESSAGE, reply_markup=cancel_keyboard())
            else:
                await callback.message.answer(GEO_MESSAGE, reply_markup=skip_keyboard())


async def check_order_task(message: types.Message, state: FSMContext):
    state_type = await state.get_state()

    if message.text == ALL_TASK_GOOD:
        match state_type:
            case StateDefaultCreo.check.state:
                await StateDefaultCreo.deadline.set()
                await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())
            case StateAppCreo.check.state:
                await StateAppCreo.deadline.set()
                await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())
            case StateOtherCreo.check.state:
                await StateOtherCreo.deadline.set()
                await message.answer(DEADLINE_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.finish()
        await StateOrderCreo.format_creo.set()
        await message.answer(DESIGN_FORMAT, reply_markup=design_format_keyboard())


async def check_size_message_creo(message, task_data, state):
    try:
        await message.answer(check_view_order(task_data), reply_markup=check_task_view_keyboard())
    except MessageIsTooLong as e:
        print(f"MessageIsTooLong error: ({e}) for {message.chat.id}")
        await message.answer(MESSAGE_IS_TOO_LONG, reply_markup=check_task_view_keyboard())
        await state.reset_state()
        await StateOrderCreo.format_creo.set()
        await message.answer(DESIGN_FORMAT, reply_markup=design_format_keyboard())
