from aiogram.fsm.state import StatesGroup, State


class CreatePWAState(StatesGroup):
    Geo = State()
    Name = State()
    Desc = State()

