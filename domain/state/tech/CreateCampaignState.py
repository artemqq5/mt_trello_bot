from aiogram.fsm.state import StatesGroup, State


class CreateCampaignState(StatesGroup):
    Geo = State()
    AppName = State()
