from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import TECH_ACCESS
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.OrderTechState import OrderTechState
from presentation.keyboards.tech.kb_order_tech import kb_choice_category_tech

router = Router()

# router.include_routers()

router.message.middleware(IsRoleMiddleware(TECH_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(TECH_ACCESS))


@router.message(F.text == L.TASK_TECH())
async def order_tech(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(OrderTechState.Category)
    await message.answer(i18n.TECH.CHOICE_CATEGORY(), reply_markup=kb_choice_category_tech)

