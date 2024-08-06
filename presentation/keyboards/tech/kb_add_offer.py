from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L, I18nContext
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup


class ChoiceAdvertiserType(CallbackData, prefix="ChoiceAdvertiserType"):
    advertiser: str


def kb_choice_advertiser_type(i18n: I18nContext):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L.TECH.ADVERTISER_NEW(), callback_data=ChoiceAdvertiserType(advertiser=i18n.TECH.ADVERTISER_NEW()).pack())],
        [InlineKeyboardButton(text=L.TECH.ADVERTISER_EXISTING(), callback_data=ChoiceAdvertiserType(advertiser=i18n.TECH.ADVERTISER_EXISTING()).pack())]
    ])
