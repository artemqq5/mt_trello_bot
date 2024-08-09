from aiogram.fsm.state import StatesGroup, State


class MyTaskState(StatesGroup):
    ChoiceTask = State()
    Comment = State()
    Delete = State()
