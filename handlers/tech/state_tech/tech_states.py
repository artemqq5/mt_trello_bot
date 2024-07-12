from aiogram.dispatcher.filters.state import StatesGroup, State


class StateTechTask(StatesGroup):
    set_task = State()
    choice_tech = State()


class StateAddOffer(StatesGroup):
    advertiser_type = State()
    tg_group = State()
    advertiser_name = State()
    offer_name = State()
    geo = State()
    geo_deduction = State()
    promo_link = State()


class StateCreateCampaign(StatesGroup):
    geo = State()
    app_name = State()


class StateEditOffer(StatesGroup):
    offer_id = State()
    desc = State()


class StateMTPartners(StatesGroup):
    desc = State()
    deadline = State()


class StateOtherTask(StatesGroup):
    desc = State()
    deadline = State()


class StatePrepareVait(StatesGroup):
    geo = State()
    source = State()
    technical_task_link = State()
    desc = State()
    deadline = State()


class StateCreatePWA(StatesGroup):
    geo = State()
    name = State()
    desc = State()
    deadline = State()


class StateSetDomain(StatesGroup):
    offers_name = State()
    desc = State()
    deadline = State()


class StateSettingCloak(StatesGroup):
    geo = State()
    offer = State()
    domains = State()
    desc = State()


class StateShareApp(StatesGroup):
    name = State()
    id_cabinets = State()
    desc = State()

