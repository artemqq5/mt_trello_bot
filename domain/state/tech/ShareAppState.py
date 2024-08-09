from aiogram.fsm.state import StatesGroup, State


class ShareAppState(StatesGroup):
    Name = State()
    CabinetIDs = State()
    Desc = State()

