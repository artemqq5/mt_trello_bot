from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup


class TypeCreo(CallbackData, prefix="TypeCreo"):
    type_creo: str


kb_set_type_creo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.CREO.VIDEO(), callback_data=TypeCreo(type_creo="Video").pack())],
    [InlineKeyboardButton(text=L.CREO.STATIC(), callback_data=TypeCreo(type_creo="Static").pack())],
    [InlineKeyboardButton(text=L.CREO.GIF(), callback_data=TypeCreo(type_creo="GIF").pack())],
])


class PlatformCreo(CallbackData, prefix="PlatformCreo"):
    platform: str


kb_set_platform_creo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.CREO.APPSTORE(), callback_data=PlatformCreo(platform="AppStore").pack())],
    [InlineKeyboardButton(text=L.CREO.GOOGLEPLAY(), callback_data=PlatformCreo(platform="GooglePlay").pack())],
])


class SendTaskCreo(CallbackData, prefix="SendTaskCreo"):
    pass


class StartAgainCreo(CallbackData, prefix="StartAgainCreo"):
    pass


def kb_preview_creo(data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L.CREO.PREVIEW_SEND(), callback_data=SendTaskCreo(data=data).pack())],
        [InlineKeyboardButton(text=L.CREO.PREVIEW_RETURN(), callback_data=StartAgainCreo().pack())]
    ])


class SkipDeadlineCreo(CallbackData, prefix="SkipDeadlineCreo"):
    pass


kb_skip_creo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.SKIP(), callback_data=SkipDeadlineCreo().pack())]
])
