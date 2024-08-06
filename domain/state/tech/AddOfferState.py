from aiogram.fsm.state import StatesGroup, State


class AddOfferState(StatesGroup):
    AdvertiserType = State()
    TelegramGroup = State()
    AdvertiserName = State()
    OfferName = State()
    Geo = State()
    GeoPrice = State()
    PromoLink = State()

