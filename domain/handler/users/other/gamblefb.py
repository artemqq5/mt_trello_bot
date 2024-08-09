from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import *
from data.repository.TrelloRepository import TrelloRepository
from domain.filter.IsDepFilter import IsDepFilter
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.aff.OrderAffState import OrderAffState
from domain.state.creo.OrderCreoState import OrderCreoState
from domain.state.my_task.MyTaskState import MyTaskState
from presentation.keyboards.creo.kb_order_creo import kb_set_type_creo, StartAgainCreo
from presentation.keyboards.kb_menu import kb_menu_all
from presentation.keyboards.my_task.kb_my_task import kb_show_task
from presentation.keyboards.tech.kb_order_tech import kb_category_tech_gamblefb

router = Router()

router.message.middleware(IsRoleMiddleware((GAMBLE_FB,)))
router.callback_query.middleware(IsRoleMiddleware((GAMBLE_FB,)))


@router.message(Command("start"), IsDepFilter((GAMBLE_FB,)))
async def start(message: Message, state: FSMContext, i18n: I18nContext):
    await message.answer(i18n.START(), reply_markup=kb_menu_all)


@router.message(F.text == L.TASK_TECH(), IsDepFilter((GAMBLE_FB,)))
async def order_tech_start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await message.answer(i18n.TECH.CHOICE_CATEGORY(), reply_markup=kb_category_tech_gamblefb)


@router.message(F.text == L.TASK_AFF(), IsDepFilter((GAMBLE_FB,)))
async def order_aff_start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(OrderAffState.Desc)
    await message.answer(i18n.AFF.DESC_OFFER())


@router.message(F.text == L.TASK_CREO(), IsDepFilter((GAMBLE_FB,)))
async def order_creo_start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(OrderCreoState.Type)
    await message.answer(i18n.CREO.SET_TYPE(), reply_markup=kb_set_type_creo)


@router.callback_query(StartAgainCreo.filter(), OrderCreoState.Preview, IsDepFilter((GAMBLE_FB,)))
async def restart_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await order_creo_start(callback.message, state, i18n)


@router.message(F.text == L.MY_TASK(), IsDepFilter((GAMBLE_FB,)))
async def my_tasks(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(MyTaskState.ChoiceTask)
    await message.answer(
        i18n.MY_TASK.VIEW(),
        reply_markup=kb_show_task(tasks=TrelloRepository().get_all_cards_by_user(message.from_user.id, i18n))
    )

