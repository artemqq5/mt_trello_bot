import math

from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup


class TechTaskInfo(CallbackData, prefix="TechTaskInfo"):
    id_: int


class CreoTaskInfo(CallbackData, prefix="CreoTaskInfo"):
    id_: int


class MyTaskNav(CallbackData, prefix="MyTaskNav"):
    page: int


def kb_show_task(tasks, current_page=1):
    inline_kb = []

    total_pages = math.ceil(len(tasks) / 8)
    start_index = (current_page - 1) * 8
    end_index = min(start_index + 8, len(tasks))

    # load from db
    for i in range(start_index, end_index):
        callback = CreoTaskInfo(id_=tasks[i]['id']) if tasks[i].get('type', None) else TechTaskInfo(id_=tasks[i]['id'])
        inline_kb.append(
            [InlineKeyboardButton(
                text=L.MY_TASK.TASK_LIST_TEMPLATE(
                    id=tasks[i]['id'],
                    category=tasks[i]['category'],
                    emoji=tasks[i]['emoji']
                ),
                callback_data=callback.pack()
            )]
        )

    nav = []

    # Navigation buttons
    if current_page > 1:
        nav.append(InlineKeyboardButton(
            text='<',
            callback_data=MyTaskNav(page=current_page - 1).pack()
        ))
    else:
        nav.append(InlineKeyboardButton(
            text='<',
            callback_data="None"
        ))

    nav.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="None"))

    if current_page < total_pages:
        nav.append(InlineKeyboardButton(
            text='>',
            callback_data=MyTaskNav(page=current_page + 1).pack()
        ))
    else:
        nav.append(InlineKeyboardButton(
            text='>',
            callback_data="None"
        ))

    if len(tasks) > 8:
        inline_kb.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


class CommentTask(CallbackData, prefix="CommentTask"):
    id_card: str


class DeleteTask(CallbackData, prefix="DeleteTask"):
    id_card: str


class MyTaskBack(CallbackData, prefix="MyTaskBack"):
    pass


def kb_manage_task(id_):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L.BACK(), callback_data=MyTaskBack().pack())],
        [InlineKeyboardButton(text=L.MY_TASK.COMMENT(), callback_data=CommentTask(id_card=id_).pack())],
        [InlineKeyboardButton(text=L.MY_TASK.DELETE(), callback_data=DeleteTask(id_card=id_).pack())],
    ])


kb_comment_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.BACK(), callback_data=MyTaskBack().pack())]
])


class MyTaskDeleteYES(CallbackData, prefix="MyTaskDeleteYES"):
    pass


kb_delete_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.BACK(), callback_data=MyTaskBack().pack())],
    [InlineKeyboardButton(text=L.MY_TASK.DELETE_YES(), callback_data=MyTaskDeleteYES().pack())]
])
