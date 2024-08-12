from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, L

from data.const import *
from data.repository.TrelloRepository import TrelloRepository
from domain.filter.IsDepFilter import IsDepFilter
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.my_task.MyTaskState import MyTaskState
from presentation.keyboards.kb_menu import kb_menu_tech
from presentation.keyboards.my_task.kb_my_task import kb_show_task
from presentation.keyboards.tech.kb_order_tech import kb_category_tech_mt_partners

router = Router()

router.message.middleware(IsRoleMiddleware((MT_PARTNERS,)))
router.callback_query.middleware(IsRoleMiddleware((MT_PARTNERS,)))


@router.message(Command("start"), IsDepFilter((MT_PARTNERS,)))
async def start(message: Message, state: FSMContext, i18n: I18nContext):
    await message.answer(i18n.START(), reply_markup=kb_menu_tech)


@router.message(F.text == L.TASK_TECH(), IsDepFilter((MT_PARTNERS,)))
async def order_tech_start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await message.answer(i18n.TECH.CHOICE_CATEGORY(), reply_markup=kb_category_tech_mt_partners)


@router.message(F.text == L.MY_TASK(), IsDepFilter((MT_PARTNERS,)))
async def my_tasks(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(MyTaskState.ChoiceTask)
    await message.answer(
        i18n.MY_TASK.VIEW(),
        reply_markup=kb_show_task(tasks=TrelloRepository().get_all_cards_by_user(message.from_user.id, i18n))
    )
