from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.ConfigurateCloakState import ConfigurateCloakState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechConfigurateCloak, kb_tech_choice

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_UAC_PPC]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_UAC_PPC]))


@router.callback_query(TechConfigurateCloak.filter())
async def configurate_cloak_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(ConfigurateCloakState.Geo)
    await state.update_data(category=i18n.TECH.CONFIGURATE_CLOAK())
    await callback.message.answer(i18n.TECH.CONFIGURATE_CLOAK.GEO())


@router.message(ConfigurateCloakState.Geo)
async def configurate_cloak_geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo=message.text)
    await state.set_state(ConfigurateCloakState.Offer)
    await message.answer(i18n.TECH.CONFIGURATE_CLOAK.OFFER())


@router.message(ConfigurateCloakState.Offer)
async def configurate_cloak_offer(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(offer=message.text)
    await state.set_state(ConfigurateCloakState.Domains)
    await message.answer(i18n.TECH.CNFIGURATE_CLOAK.DOMAINS())


@router.message(ConfigurateCloakState.Domains)
async def configurate_cloak_domains(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(domains=message.text)
    await state.set_state(ConfigurateCloakState.Desc)
    await message.answer(i18n.TECH.CONFIGURATE_CLOAK.DESC())


@router.message(ConfigurateCloakState.Desc)
async def configurate_cloak_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.CONFIGURATE_CLOAK.CARD_DESC(
            geo=data['geo'],
            offer=data['offer'],
            domains=data['domains'],
            desc=data['desc']
        )
    )

    await state.set_state(TechTaskState.ChoiceTech)
    await message.answer(i18n.TECH.CHOICE_TECH(), reply_markup=kb_tech_choice())
