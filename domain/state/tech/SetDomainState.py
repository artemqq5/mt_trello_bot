from aiogram.fsm.state import StatesGroup, State


class SetDomainState(StatesGroup):
    OfferName = State()
    Desc = State()
