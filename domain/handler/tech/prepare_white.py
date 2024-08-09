from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.PrepareWhiteState import PrepareWhiteState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechPrepareWhite, kb_skip_deadline_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_UAC_PPC]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_UAC_PPC]))


@router.callback_query(TechPrepareWhite.filter())
async def prepare_white_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(PrepareWhiteState.Geo)
    await state.update_data(category=i18n.TECH.PREPARE_WHITE())
    await callback.message.answer(i18n.TECH.PREPARE_WHITE.GEO())


@router.message(PrepareWhiteState.Geo)
async def prepare_whaite_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo=message.text)
    await state.set_state(PrepareWhiteState.Source)
    await message.answer(i18n.TECH.PREPARE_WHITE.SOURCE())


@router.message(PrepareWhiteState.Source)
async def prepare_whaite_source(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(source=message.text)
    await state.set_state(PrepareWhiteState.TechnicalTaskLink)
    await message.answer(i18n.TECH.PREPARE_WHITE.TECHNICAL_TASK_LINK())


@router.message(PrepareWhiteState.TechnicalTaskLink)
async def prepare_whaite_tt_link(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(tt_link=message.text)
    await state.set_state(PrepareWhiteState.Desc)
    await message.answer(i18n.TECH.PREPARE_WHITE.DESC())


@router.message(PrepareWhiteState.Desc)
async def prepare_whaite_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.PREPARE_WHITE.CARD_DESC(
            geo=data['geo'],
            source=data['source'],
            tt_link=data['tt_link'],
            desc=data['desc'],
        )
    )

    await state.set_state(TechTaskState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_deadline_tech)
