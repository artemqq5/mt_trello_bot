from aiogram.fsm.state import StatesGroup, State


class AddUserState(StatesGroup):
    Name = State()
    TelegramID = State()
    Role = State()
    TDSBuyerID = State()
