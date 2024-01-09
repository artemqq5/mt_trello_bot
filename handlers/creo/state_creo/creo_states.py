from aiogram.dispatcher.filters.state import StatesGroup, State


class StateOrderCreo(StatesGroup):
    format_creo = State()
    type_creo = State()
    category_creo = State()


class StateAppCreo(StatesGroup):
    general = State()
    platform = State()
    format = State()
    offer = State()
    source = State()
    description = State()

    count = State()
    sub_description = State()

    check = State()
    deadline = State()


class StateOtherCreo(StatesGroup):
    general = State()
    format = State()
    offer = State()
    source = State()
    description = State()

    count = State()
    sub_description = State()

    check = State()
    deadline = State()


class StateDefaultCreo(StatesGroup):
    general = State()
    geo = State()
    language = State()
    currency = State()
    format = State()
    offer = State()
    voice = State()
    source = State()
    description = State()

    count = State()
    sub_description = State()

    check = State()
    deadline = State()



