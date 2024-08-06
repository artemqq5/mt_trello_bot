# from aiogram import Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, CallbackQuery
# from aiogram_i18n import I18nContext, L
#
# from data.const import TECH_ACCESS, AFF_ACCESS
# from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
# from domain.state.aff.OrderAffState import OrderAffState
#
# router = Router()
#
# # router.include_routers()
#
# router.message.middleware(IsRoleMiddleware(AFF_ACCESS))
# router.callback_query.middleware(IsRoleMiddleware(AFF_ACCESS))
#
#
# @router.message(F.text == L.TASK_AFF())
# async def order_aff_start(message: Message, state: FSMContext, i18n: I18nContext):
#     await state.clear()
#     await state.set_state(OrderAffState.Offer)
#     # await message.answer(i18n.TECH.CHOICE_CATEGORY(), reply_markup=kb_choice_category_tech)
#
