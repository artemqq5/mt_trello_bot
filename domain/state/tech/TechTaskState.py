from aiogram.fsm.state import StatesGroup, State


class TechTaskState(StatesGroup):
    DeadLine = State()
    ChoiceTech = State()
