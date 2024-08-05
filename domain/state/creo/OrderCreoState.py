from aiogram.fsm.state import StatesGroup, State


class OrderCreoState(StatesGroup):
    Type = State()
    Category = State()
    Geo = State()
    Lang = State()
    Currency = State()
    Format = State()
    Offer = State()
    Voice = State()
    Source = State()
    Desc = State()
    Platform = State()
    Count = State()
    DeadLine = State()
    Preview = State()

