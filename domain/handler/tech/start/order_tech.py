from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import TECH_ACCESS
from data.repository.TechRepository import TechRepository
from data.repository.TrelloRepository import TrelloRepository
from data.repository.UserRepository import UserRepository
from domain.handler.tech import add_offer
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.TechTaskState import TechTaskState
from domain.use_case.NotificationUsers import NotificationUsers
from presentation.keyboards.tech.kb_order_tech import kb_choice_category_tech, ChoiceTech

router = Router()

router.include_routers(
    add_offer.router,
)

router.message.middleware(IsRoleMiddleware(TECH_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(TECH_ACCESS))


@router.callback_query(ChoiceTech.filter(), TechTaskState.ChoiceTech)
async def choice_tech(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    tech = callback.data.split(":")[1]
    await state.update_data(tech=tech)

    data = await state.update_data()
    user = UserRepository().user(callback.from_user.id)

    if not (card_id := TrelloRepository().create_tech_task(data, user, i18n)):
        await callback.answer(i18n.ERROR_CREATE_CARD(), show_alert=True)
        return

    card = TechRepository().card(card_id)

    await NotificationUsers.notify_new_tech(callback, card, i18n)

