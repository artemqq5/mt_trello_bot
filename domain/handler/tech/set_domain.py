from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.SetDomainState import SetDomainState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechSetDomain, kb_skip_deadline_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_UAC_PPC]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_UAC_PPC]))


@router.callback_query(TechSetDomain.filter())
async def set_domain_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(SetDomainState.OfferName)
    await state.update_data(category=i18n.TECH.SET_DOMAIN())
    await callback.message.answer(i18n.TECH.SET_DOMAIN.OFFER_NAME())


@router.message(SetDomainState.OfferName)
async def set_domain_offer_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(offer_name=message.text)
    await state.set_state(SetDomainState.Desc)
    await message.answer(i18n.TECH.SET_DOMAIN.DESC())


@router.message(SetDomainState.Desc)
async def set_domain_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.SET_DOMAIN.CARD_DESC(
            offer_name=data['offer_name'],
            desc=data['desc'],
        )
    )

    await state.set_state(TechTaskState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_deadline_tech)
