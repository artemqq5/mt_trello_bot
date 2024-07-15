from aiogram import types
from aiogram.dispatcher import FSMContext

from _keyboard.tech_keyboard.tech_keyboard import tech_choice
from constants.tech import CHOICE_TECH
from handlers.tech.state_tech.tech_states import StateTechTask
from handlers.tech.tools.send_task import send_order_tech


def register_choice_tech_handler(dispatcher):
    dispatcher.register_callback_query_handler(
        choice_tech_callback,
        lambda call: "ChoiceTechTask" in call.data,
        state=StateTechTask.choice_tech
    )


async def choice_tech_callback(callback: types.CallbackQuery, state: FSMContext):
    tech = callback.data.split(":")[1]
    data = await state.get_data()

    await send_order_tech(data=data, message=callback.message, type_=data['type_task'], tech=tech)
    await state.finish()
