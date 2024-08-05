from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.const import ALL_DEP
from data.repository.UserRepository import UserRepository


class ShowUser(CallbackData, prefix="ShowUser"):
    id_user: str


class ShowUserNav(CallbackData, prefix="ShowUserNav"):
    page: int


class ShowUserBack(CallbackData, prefix="ShowUserBack"):
    pass


def kb_show_users(current_page=1):
    inline_kb = []

    categories = list(dep for dep in ALL_DEP if UserRepository().users_by_dep(dep))
    index = min(current_page - 1, len(categories))

    # load from db
    for user in UserRepository().users_by_dep(categories[index]):
        inline_kb.append(
            [InlineKeyboardButton(
                text=f"{user['name_user']}",
                callback_data=ShowUser(id_user=user['id_user']).pack()
            )]
        )

    if len(categories) > 1:
        nav = []
        # Navigation buttons
        if current_page > 1:
            nav.append(InlineKeyboardButton(
                text='<',
                callback_data=ShowUserNav(page=current_page - 1).pack()
            ))
        else:
            nav.append(InlineKeyboardButton(
                text='<',
                callback_data="None"
            ))

        nav.append(InlineKeyboardButton(text=f"{current_page}/{len(categories)}", callback_data="None"))

        if current_page < len(categories):
            nav.append(InlineKeyboardButton(
                text='>',
                callback_data=ShowUserNav(page=current_page + 1).pack()
            ))
        else:
            nav.append(InlineKeyboardButton(
                text='>',
                callback_data="None"
            ))

        inline_kb.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def text_users_category(current_page=1):
    categories = list(dep for dep in ALL_DEP if UserRepository().users_by_dep(dep))
    index = min(current_page-1, len(categories))
    return f"<b>{categories[index]}</b>"


kb_user_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.BACK(), callback_data=ShowUserBack().pack())]
])
