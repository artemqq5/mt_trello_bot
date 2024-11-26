from aiogram.fsm.state import StatesGroup, State


class AdminSystemState(StatesGroup):
    DeleteUser = State()
    GetAll = State()
    MailingAll = State()
    

