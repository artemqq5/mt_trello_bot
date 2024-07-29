from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMyTaskManage(StatesGroup):
    start_manage = State()
    comment = State()

