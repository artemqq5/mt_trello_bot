from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import TECH_ACCESS, AFF_ACCESS
from data.repository.AffRepository import AffRepository
from data.repository.TrelloRepository import TrelloRepository
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.aff.OrderAffState import OrderAffState
from domain.use_case.NotificationUsers import NotificationUsers

router = Router()

router.message.middleware(IsRoleMiddleware(AFF_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(AFF_ACCESS))


@router.message(OrderAffState.Desc)
async def order_aff_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        desc=data['desc'],
    )

    data = await state.update_data()
    user = UserRepository().user(message.from_user.id)

    await message.delete()

    if not (card_id := TrelloRepository().create_aff_task(data, user, i18n)):
        await message.answer(i18n.ERROR_CREATE_CARD(), show_alert=True)
        return

    card = AffRepository().card(card_id)

    await NotificationUsers.notify_new_aff(message, card, i18n)
    await message.answer(i18n.TASK_SEND_SUCCESS())


