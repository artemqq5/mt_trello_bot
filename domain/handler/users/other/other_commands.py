# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
# from aiogram_i18n import I18nContext
#
# from data.const import USERS
#
# from domain.filter.IsDepFilter import IsDepFilter
# from domain.handler.creo import order_creo
# from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
# from presentation.keyboards.kb_menu import kb_menu_all
#
# router = Router()
#
# router.message.middleware(IsRoleMiddleware(USERS))
# router.callback_query.middleware(IsRoleMiddleware(USERS))
#
#
# @router.message(Command("start"), IsDepFilter(USERS))
# async def start(message: Message, state: FSMContext, i18n: I18nContext):
#     await message.answer(i18n.START(), reply_markup=kb_menu_all)
