from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.EditOfferState import EditOfferState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechEditOffer, kb_tech_choice

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, AFMNGR]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, AFMNGR]))


@router.callback_query(TechEditOffer.filter())
async def create_campaign_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(EditOfferState.OfferID)
    await state.update_data(category=i18n.TECH.EDIT_OFFER())
    await callback.message.answer(i18n.TECH.EDIT_OFFER.OFFER_ID())


@router.message(EditOfferState.OfferID)
async def configurate_cloak_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(offer_id=message.text)
    await state.set_state(EditOfferState.Desc)
    await message.answer(i18n.TECH.EDIT_OFFER.DESC())


@router.message(EditOfferState.Desc)
async def configurate_cloak_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.EDIT_OFFER.CARD_DESC(
            offer_id=data['offer_id'],
            desc=data['desc']
        )
    )

    await state.set_state(TechTaskState.ChoiceTech)
    await message.answer(i18n.TECH.CHOICE_TECH(), reply_markup=kb_tech_choice())
