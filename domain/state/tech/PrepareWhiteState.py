from aiogram.fsm.state import StatesGroup, State


class PrepareWhiteState(StatesGroup):
    Geo = State()
    Source = State()
    TechnicalTaskLink = State()
    Desc = State()
