from aiogram.fsm.state import StatesGroup, State


class BotTaskState(StatesGroup):
    Name = State()
    Desc = State()

