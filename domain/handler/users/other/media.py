from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import *
from domain.filter.IsDepFilter import IsDepFilter
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.creo.OrderCreoState import OrderCreoState
from presentation.keyboards.creo.kb_order_creo import kb_set_type_creo, StartAgainCreo
from presentation.keyboards.kb_menu import kb_menu_design

router = Router()

router.message.middleware(IsRoleMiddleware((MEDIA,)))
router.callback_query.middleware(IsRoleMiddleware((MEDIA,)))


@router.message(Command("start"), IsDepFilter((MEDIA,)))
async def start(message: Message, state: FSMContext, i18n: I18nContext):
    await message.answer(i18n.START(), reply_markup=kb_menu_design)


@router.message(F.text == L.TASK_CREO(), IsDepFilter((MEDIA,)))
async def order_creo_start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(OrderCreoState.Type)
    await message.answer(i18n.CREO.SET_TYPE(), reply_markup=kb_set_type_creo)


@router.callback_query(StartAgainCreo.filter(), OrderCreoState.Preview, IsDepFilter((MEDIA,)))
async def restart_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await order_creo_start(callback.message, state, i18n)
