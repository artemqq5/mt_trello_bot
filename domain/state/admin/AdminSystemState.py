from aiogram.fsm.state import StatesGroup, State


class AdminSystemState(StatesGroup):
    AddUser = State()
    DeleteUser = State()
    GetAll = State()
    MailingAll = State()
    

