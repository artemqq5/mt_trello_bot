from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L, I18nContext
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup


class TechAddOffer(CallbackData, prefix="TechAddOffer"):
    pass


class TechConfigurateCloak(CallbackData, prefix="TechConfigurateCloak"):
    pass


class TechCreateCampaign(CallbackData, prefix="TechCreateCampaign"):
    pass


class TechEditOffer(CallbackData, prefix="TechEditOffer"):
    pass


class TechMTPartners(CallbackData, prefix="TechMTPartners"):
    pass


class TechPrepareWhite(CallbackData, prefix="TechPrepareWhite"):
    pass


class TechCreatePWA(CallbackData, prefix="TechCreatePWA"):
    pass


class TechSetDomain(CallbackData, prefix="TechSetDomain"):
    pass


class TechShareApp(CallbackData, prefix="TechShareApp"):
    pass


class TechOtherTask(CallbackData, prefix="TechOtherTask"):
    pass


kb_category_tech_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.ADD_OFFER(), callback_data=TechAddOffer().pack())],
    [InlineKeyboardButton(text=L.TECH.CONFIGURATE_CLOAK(), callback_data=TechConfigurateCloak().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_CAMPAIGN(), callback_data=TechCreateCampaign().pack())],
    [InlineKeyboardButton(text=L.TECH.EDIT_OFFER(), callback_data=TechEditOffer().pack())],
    [InlineKeyboardButton(text=L.TECH.MT_PARTNERS(), callback_data=TechMTPartners().pack())],
    [InlineKeyboardButton(text=L.TECH.PREPARE_WHITE(), callback_data=TechPrepareWhite().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_PWA(), callback_data=TechCreatePWA().pack())],
    [InlineKeyboardButton(text=L.TECH.SET_DOMAIN(), callback_data=TechSetDomain().pack())],
    [InlineKeyboardButton(text=L.TECH.SHARE_APP(), callback_data=TechShareApp().pack())],
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])

kb_category_tech_gambleppc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.CONFIGURATE_CLOAK(), callback_data=TechConfigurateCloak().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_CAMPAIGN(), callback_data=TechCreateCampaign().pack())],
    [InlineKeyboardButton(text=L.TECH.PREPARE_WHITE(), callback_data=TechPrepareWhite().pack())],
    [InlineKeyboardButton(text=L.TECH.SET_DOMAIN(), callback_data=TechSetDomain().pack())],
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])

kb_category_tech_gamblefb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.CREATE_CAMPAIGN(), callback_data=TechCreateCampaign().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_PWA(), callback_data=TechCreatePWA().pack())],
    [InlineKeyboardButton(text=L.TECH.SHARE_APP(), callback_data=TechShareApp().pack())],
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])

kb_category_tech_gambleuac = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.CREATE_CAMPAIGN(), callback_data=TechCreateCampaign().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_PWA(), callback_data=TechCreatePWA().pack())],
    [InlineKeyboardButton(text=L.TECH.SHARE_APP(), callback_data=TechShareApp().pack())],
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])

kb_category_tech_gambleuac_ppc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.CONFIGURATE_CLOAK(), callback_data=TechConfigurateCloak().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_CAMPAIGN(), callback_data=TechCreateCampaign().pack())],
    [InlineKeyboardButton(text=L.TECH.PREPARE_WHITE(), callback_data=TechPrepareWhite().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_PWA(), callback_data=TechCreatePWA().pack())],
    [InlineKeyboardButton(text=L.TECH.SET_DOMAIN(), callback_data=TechSetDomain().pack())],
    [InlineKeyboardButton(text=L.TECH.SHARE_APP(), callback_data=TechShareApp().pack())],
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])

kb_category_tech_afmngr = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.ADD_OFFER(), callback_data=TechAddOffer().pack())],
    [InlineKeyboardButton(text=L.TECH.EDIT_OFFER(), callback_data=TechEditOffer().pack())],
])

kb_category_tech_mt_partners = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.MT_PARTNERS(), callback_data=TechMTPartners().pack())],
])

kb_category_tech_dev = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])


class ChoiceTech(CallbackData, prefix="ChoiceTech"):
    tech: str


def kb_tech_choice():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L.TECH.GLEB(), callback_data=ChoiceTech(tech="Gleb").pack())],
        [InlineKeyboardButton(text=L.TECH.EGOR(), callback_data=ChoiceTech(tech="Egor").pack())]
    ])


class SkipDeadLineTech(CallbackData, prefix="SkipDeadLineTech"):
    pass


kb_skip_deadline_tech = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.SKIP(), callback_data=SkipDeadLineTech().pack())]
])
