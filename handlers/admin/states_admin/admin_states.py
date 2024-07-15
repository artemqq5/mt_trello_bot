from aiogram.dispatcher.filters.state import StatesGroup, State


class StateAddUser(StatesGroup):
    add_user = State()


class StateDeleteUser(StatesGroup):
    delete_user = State()


class StateGetAllUsers(StatesGroup):
    get_all_users = State()


class StateMailingAllUsers(StatesGroup):
    mailing_all_users = State()
