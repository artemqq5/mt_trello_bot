from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, L

from data.const import *
from domain.filter.IsDepFilter import IsDepFilter
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from presentation.keyboards.kb_menu import kb_menu_tech
from presentation.keyboards.tech.kb_order_tech import kb_category_tech_afmngr

router = Router()

router.message.middleware(IsRoleMiddleware((AFMNGR,)))
router.callback_query.middleware(IsRoleMiddleware((AFMNGR,)))


@router.message(Command("start"), IsDepFilter((AFMNGR,)))
async def start(message: Message, state: FSMContext, i18n: I18nContext):
    await message.answer(i18n.START(), reply_markup=kb_menu_tech)


@router.message(F.text == L.TASK_TECH(), IsDepFilter((AFMNGR,)))
async def order_tech_start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await message.answer(i18n.TECH.CHOICE_CATEGORY(), reply_markup=kb_category_tech_afmngr)


