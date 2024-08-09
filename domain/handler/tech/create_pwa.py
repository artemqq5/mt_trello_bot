from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.CreatePWAState import CreatePWAState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechCreatePWA, kb_skip_deadline_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC]))


@router.callback_query(TechCreatePWA.filter())
async def create_pwa_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(CreatePWAState.Geo)
    await state.update_data(category=i18n.TECH.CREATE_PWA())
    await callback.message.answer(i18n.TECH.CREATE_PWA.GEO())


@router.message(CreatePWAState.Geo)
async def create_pwa_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo=message.text)
    await state.set_state(CreatePWAState.Name)
    await message.answer(i18n.TECH.CREATE_PWA.NAME())


@router.message(CreatePWAState.Name)
async def create_pwa_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(name=message.text)
    await state.set_state(CreatePWAState.Desc)
    await message.answer(i18n.TECH.CREATE_PWA.DESC())


@router.message(CreatePWAState.Desc)
async def create_pwa_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.CREATE_PWA.CARD_DESC(
            geo=data['geo'],
            name=data['name'],
            desc=data['desc']
        )
    )

    await state.set_state(TechTaskState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_deadline_tech)
