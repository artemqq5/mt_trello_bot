from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware

from domain.state.tech.AddOfferState import AddOfferState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_add_offer import kb_choice_advertiser_type, ChoiceAdvertiserType
from presentation.keyboards.tech.kb_order_tech import kb_choice_category_tech, TechAddOffer, kb_tech_choice

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, AFMNGR]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, AFMNGR]))


@router.callback_query(TechAddOffer.filter())
async def add_offer_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(AddOfferState.AdvertiserType)
    await state.update_data(category=i18n.TECH.ADD_OFFER())
    await callback.message.edit_text(i18n.TECH.CHOICE_ADVERTISER_TYPE(), reply_markup=kb_choice_advertiser_type(i18n))


@router.callback_query(ChoiceAdvertiserType.filter(), AddOfferState.AdvertiserType)
async def set_advertiser_type(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    advertiser_type = callback.data.split(":")[1]
    await state.update_data(advertiser_type=advertiser_type)

    if advertiser_type == i18n.TECH.ADVERTISER_NEW():
        await state.set_state(AddOfferState.TelegramGroup)
        await callback.message.answer(i18n.TECH.TELEGRAM_GROUP())
    else:
        await state.set_state(AddOfferState.AdvertiserName)
        await callback.message.answer(i18n.TECH.ADVERTISER_NAME())


@router.message(AddOfferState.TelegramGroup)
async def set_telegram_group(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(telegram_group=message.text)
    await state.set_state(AddOfferState.AdvertiserName)
    await message.answer(i18n.TECH.ADVERTISER_NAME())


@router.message(AddOfferState.AdvertiserName)
async def set_advertiser_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(advertiser_name=message.text)
    await state.set_state(AddOfferState.OfferName)
    await message.answer(i18n.TECH.OFFER_NAME())


@router.message(AddOfferState.OfferName)
async def set_offer_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(offer_name=message.text)
    await state.set_state(AddOfferState.Geo)
    await message.answer(i18n.TECH.GEO())


@router.message(AddOfferState.Geo)
async def set_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo=message.text)
    await state.set_state(AddOfferState.GeoPrice)
    await message.answer(i18n.TECH.GEO_PRICE())


@router.message(AddOfferState.GeoPrice)
async def set_geo_price(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo_price=message.text)
    await state.set_state(AddOfferState.PromoLink)
    await message.answer(i18n.TECH.PROMO_LINK())


@router.message(AddOfferState.PromoLink)
async def set_promo_link(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(promo_link=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.ADD_OFFER.CARD_DESC(
            type=data['advertiser_type'],
            tg=data.get('telegram_group', "-"),
            adv_name=data['advertiser_name'],
            offer_name=data['offer_name'],
            geo=data['geo'],
            geo_price=data['geo_price'],
            promo=data['promo_link'],
            username=message.from_user.username
        )
    )

    await state.set_state(TechTaskState.ChoiceTech)
    await message.answer(i18n.TECH.CHOICE_TECH(), reply_markup=kb_tech_choice(i18n))

