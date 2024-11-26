from aiogram.filters.callback_data import CallbackData
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.const import *


class UserRoleCallback(CallbackData, prefix="UserRoleCallback"):
    role: str


kb_user_role = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=ADMIN, callback_data=UserRoleCallback(role=ADMIN).pack())],
    [InlineKeyboardButton(text=GAMBLE_PPC, callback_data=UserRoleCallback(role=GAMBLE_PPC).pack())],
    [InlineKeyboardButton(text=GAMBLE_UAC, callback_data=UserRoleCallback(role=GAMBLE_UAC).pack())],
    [InlineKeyboardButton(text=GAMBLE_FB, callback_data=UserRoleCallback(role=GAMBLE_FB).pack())],
    [InlineKeyboardButton(text=AFMNGR, callback_data=UserRoleCallback(role=AFMNGR).pack())],
    [InlineKeyboardButton(text=MEDIA, callback_data=UserRoleCallback(role=MEDIA).pack())],
    [InlineKeyboardButton(text=GAMBLE_UAC_PPC, callback_data=UserRoleCallback(role=GAMBLE_UAC_PPC).pack())],
    [InlineKeyboardButton(text=MT_PARTNERS, callback_data=UserRoleCallback(role=MT_PARTNERS).pack())],
    [InlineKeyboardButton(text=DEV, callback_data=UserRoleCallback(role=DEV).pack())],
    [InlineKeyboardButton(text=DESIGNER, callback_data=UserRoleCallback(role=DESIGNER).pack())],
    [InlineKeyboardButton(text=TECH, callback_data=UserRoleCallback(role=TECH).pack())],
])
