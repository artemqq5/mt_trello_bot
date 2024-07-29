import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.base_keyboard import skip_keyboard, cancel_keyboard
from _keyboard.creo_keyboard.creo_keyboard import check_task_view_keyboard
from constants.base import SKIP, WRONG_TIME_CHOICE
from constants.creo import LANGUAGE_MESSAGE, ADAPTIVE_CREATIVE, CURRENCY_MESSAGE, FORMAT_MESSAGE, OFFER_MESSAGE, \
    VOICE_MESSAGE, SOURCE_MESSAGE, DESCRIPTION_MESSAGE, COUNT_OF_CREO, WRONG_FORMAT_INPUT_CREO, SUB_DESC_FOR_OTHER_CREO
from handlers.creo.start_order import check_size_message_creo
from handlers.creo.state_creo.creo_states import StateDefaultCreo
from handlers.creo.tools.message_tools import check_view_order
from handlers.creo.tools.send_task import send_order_creo


def register_default_creo_handlers(dispatcher):
    dispatcher.register_message_handler(set_geo_default, state=StateDefaultCreo.geo)
    dispatcher.register_message_handler(set_language_default, state=StateDefaultCreo.language)
    dispatcher.register_message_handler(set_currency_default, state=StateDefaultCreo.currency)
    dispatcher.register_message_handler(set_format_default, state=StateDefaultCreo.format)
    dispatcher.register_message_handler(set_offer_default, state=StateDefaultCreo.offer)
    dispatcher.register_message_handler(set_voice_default, state=StateDefaultCreo.voice)
    dispatcher.register_message_handler(set_source_default, state=StateDefaultCreo.source)
    dispatcher.register_message_handler(set_description_default, state=StateDefaultCreo.description)
    dispatcher.register_message_handler(set_count_default, state=StateDefaultCreo.count)
    dispatcher.register_message_handler(set_sub_desc_default, state=StateDefaultCreo.sub_description)
    dispatcher.register_message_handler(set_deadline_default, state=StateDefaultCreo.deadline)


async def set_geo_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.language.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(geo=message.text)
        await message.answer(LANGUAGE_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.update_data(geo=message.text)
        await message.answer(LANGUAGE_MESSAGE, reply_markup=cancel_keyboard())


async def set_language_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.currency.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(language=message.text)
        await message.answer(CURRENCY_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.update_data(language=message.text)
        await message.answer(CURRENCY_MESSAGE, reply_markup=cancel_keyboard())


async def set_currency_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.format.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(currency=message.text)
        await message.answer(FORMAT_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.update_data(currency=message.text)
        await message.answer(FORMAT_MESSAGE, reply_markup=cancel_keyboard())


async def set_format_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.offer.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(format=message.text)
        await message.answer(OFFER_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.update_data(format=message.text)
        await message.answer(OFFER_MESSAGE, reply_markup=cancel_keyboard())


async def set_offer_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.voice.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(offer=message.text)
        await message.answer(VOICE_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.update_data(offer=message.text)
        await message.answer(VOICE_MESSAGE, reply_markup=cancel_keyboard())


async def set_voice_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.source.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(voice=message.text)
        await message.answer(SOURCE_MESSAGE, reply_markup=skip_keyboard())
    else:
        await state.update_data(voice=message.text)
        await message.answer(SOURCE_MESSAGE, reply_markup=cancel_keyboard())


async def set_source_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.description.set()
    type_creo = await state.get_data()
    if type_creo['general']['type_creo'] == ADAPTIVE_CREATIVE:
        if message.text != SKIP:
            await state.update_data(source=message.text)
    else:
        await state.update_data(source=message.text)

    await message.answer(DESCRIPTION_MESSAGE, reply_markup=cancel_keyboard())


async def set_description_default(message: types.Message, state: FSMContext):
    await StateDefaultCreo.count.set()
    await state.update_data(description=message.text)
    await message.answer(COUNT_OF_CREO, reply_markup=skip_keyboard())


async def set_count_default(message: types.Message, state: FSMContext):
    if message.text == SKIP:
        await state.update_data(count=1)
        await StateDefaultCreo.check.set()
        task_data = await state.get_data()
        await check_size_message_creo(message, task_data, state)
    else:
        try:
            count = int(message.text)
            await state.update_data(count=count)
            if count > 1:
                await StateDefaultCreo.sub_description.set()
                await message.answer(SUB_DESC_FOR_OTHER_CREO, reply_markup=cancel_keyboard())
            elif count == 1:
                await StateDefaultCreo.check.set()
                task_data = await state.get_data()
                await check_size_message_creo(message, task_data, state)
            else:
                await message.answer(WRONG_FORMAT_INPUT_CREO, reply_markup=skip_keyboard())
        except Exception as e:
            print(f"set_count_default_creative: {e}")
            await message.answer(WRONG_FORMAT_INPUT_CREO, reply_markup=skip_keyboard())


async def set_sub_desc_default(message: types.Message, state: FSMContext):
    await state.update_data(sub_description=message.text)
    await StateDefaultCreo.check.set()
    task_data = await state.get_data()
    await check_size_message_creo(message, task_data, state)


async def set_deadline_default(message: types.Message, state: FSMContext):
    if message.text != SKIP:
        try:
            date_time = datetime.datetime.strptime(message.text + " +0400", '%Y-%m-%d %H:%M %z')

            await state.update_data(deadline=str(date_time))
            data = await state.get_data()
            await state.finish()
        except Exception as e:
            print(f"set_deadline_default_creative - {e}")
            data = None
            await message.answer(WRONG_TIME_CHOICE, reply_markup=skip_keyboard())

        await send_order_creo(data, message)

    else:
        await state.update_data(deadline=None)
        data = await state.get_data()
        await state.finish()

        await send_order_creo(data, message)
