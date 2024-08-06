from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L, I18nContext
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup


class TechAddOffer(CallbackData, prefix="TechAddOffer"):
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


class TechConfigurateCloak(CallbackData, prefix="TechConfigurateCloak"):
    pass


class TechShareApp(CallbackData, prefix="TechShareApp"):
    pass


class TechOtherTask(CallbackData, prefix="TechOtherTask"):
    pass


kb_choice_category_tech = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.TECH.ADD_OFFER(), callback_data=TechAddOffer().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_CAMPAIN(), callback_data=TechCreateCampaign().pack())],
    [InlineKeyboardButton(text=L.TECH.EDIT_OFFER(), callback_data=TechEditOffer().pack())],
    [InlineKeyboardButton(text=L.TECH.MT_PARTNERS(), callback_data=TechMTPartners().pack())],
    [InlineKeyboardButton(text=L.TECH.PREPARE_WHITE(), callback_data=TechPrepareWhite().pack())],
    [InlineKeyboardButton(text=L.TECH.CREATE_PWA(), callback_data=TechCreatePWA().pack())],
    [InlineKeyboardButton(text=L.TECH.SET_DOMAIN(), callback_data=TechSetDomain().pack())],
    [InlineKeyboardButton(text=L.TECH.CONFIGURATE_CLOAK(), callback_data=TechConfigurateCloak().pack())],
    [InlineKeyboardButton(text=L.TECH.SHARE_APP(), callback_data=TechShareApp().pack())],
    [InlineKeyboardButton(text=L.TECH.OTHER_TASK(), callback_data=TechOtherTask().pack())],
])


class ChoiceTech(CallbackData, prefix="ChoiceTech"):
    tech: str


def kb_tech_choice(i18n: I18nContext):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L.TECH.GLEB(), callback_data=ChoiceTech(tech=i18n.TECH.GLEB()).pack())],
        [InlineKeyboardButton(text=L.TECH.EGOR(), callback_data=ChoiceTech(tech=i18n.TECH.EGOR()).pack())]
    ])
