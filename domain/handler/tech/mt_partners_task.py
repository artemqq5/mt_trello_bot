from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.MTPartnersState import MTPartnersState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechMTPartners, kb_skip_deadline_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, MT_PARTNERS]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, MT_PARTNERS]))


@router.callback_query(TechMTPartners.filter())
async def mt_parent_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(MTPartnersState.Desc)
    await state.update_data(category=i18n.TECH.MT_PARTNERS())
    await callback.message.answer(i18n.TECH.MT_PARTNERS.DESC())


@router.message(MTPartnersState.Desc)
async def mt_parent_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.MT_PARTNERS.CARD_DESC(
            desc=data['desc']
        )
    )

    await state.set_state(TechTaskState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_deadline_tech)
