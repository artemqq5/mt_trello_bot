from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.ShareAppState import ShareAppState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechShareApp, kb_skip_deadline_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC]))


@router.callback_query(TechShareApp.filter())
async def share_app_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(ShareAppState.Name)
    await state.update_data(category=i18n.TECH.SHARE_APP())
    await callback.message.answer(i18n.TECH.SHARE_APP.NAME())


@router.message(ShareAppState.Name)
async def share_app_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(name=message.text)
    await state.set_state(ShareAppState.CabinetIDs)
    await message.answer(i18n.TECH.SHARE_APP.CABINETS())


@router.message(ShareAppState.CabinetIDs)
async def share_app_cabinets(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(cabinets=message.text)
    await state.set_state(ShareAppState.Desc)
    await message.answer(i18n.TECH.SHARE_APP.DESC())


@router.message(ShareAppState.Desc)
async def share_app_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.SHARE_APP.CARD_DESC(
            name=data['name'],
            cabinets=data['cabinets'],
            desc=data['desc'],
        )
    )

    await state.set_state(TechTaskState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_deadline_tech)
