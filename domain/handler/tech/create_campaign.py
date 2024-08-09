from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.CreateCampaignState import CreateCampaignState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechCreateCampaign, kb_tech_choice

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC]))


@router.callback_query(TechCreateCampaign.filter())
async def create_campaign_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(CreateCampaignState.Geo)
    await state.update_data(category=i18n.TECH.CREATE_CAMPAIGN())
    await callback.message.answer(i18n.TECH.CREATE_CAMPAIGN.GEO())


@router.message(CreateCampaignState.Geo)
async def campaign_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo=message.text)
    await state.set_state(CreateCampaignState.AppName)
    await message.answer(i18n.TECH.CREATE_CAMPAIGN.APP_NAME())


@router.message(CreateCampaignState.AppName)
async def campaign_app_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(appname=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.CREATE_CAMPAIGN.CARD_DESC(
            geo=data['geo'],
            appname=data['appname']
        )
    )

    await state.set_state(TechTaskState.ChoiceTech)
    await message.answer(i18n.TECH.CHOICE_TECH(), reply_markup=kb_tech_choice())
