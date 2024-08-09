from aiogram.fsm.state import StatesGroup, State


class ConfigurateCloakState(StatesGroup):
    Geo = State()
    Offer = State()
    Domains = State()
    Desc = State()
