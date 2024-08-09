from aiogram.fsm.state import StatesGroup, State


class EditOfferState(StatesGroup):
    OfferID = State()
    Desc = State()
