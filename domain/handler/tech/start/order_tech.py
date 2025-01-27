import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from data.const import TECH_ACCESS, BUYERS_ROLE_LIST
from data.repository.TechRepository import TechRepository
from data.repository.TrelloRepository import TrelloRepository
from data.repository.UserRepository import UserRepository
from domain.handler.tech import add_offer, create_campaign, configurate_cloak, create_pwa, edit_offer, mt_partners_task, \
    other_task, prepare_white, set_domain, share_app, other_bot_task
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.TechTaskState import TechTaskState
from domain.use_case.NotificationUsers import NotificationUsers
from presentation.keyboards.tech.kb_order_tech import ChoiceTech, SkipDeadLineTech, kb_tech_choice, \
    kb_skip_deadline_tech

router = Router()

router.include_routers(
    add_offer.router,
    configurate_cloak.router,
    create_campaign.router,
    create_pwa.router,
    edit_offer.router,
    mt_partners_task.router,
    prepare_white.router,
    set_domain.router,
    share_app.router,
    other_task.router,
    other_bot_task.router
)

router.message.middleware(IsRoleMiddleware(TECH_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(TECH_ACCESS))


@router.callback_query(SkipDeadLineTech.filter(), TechTaskState.DeadLine)
async def deadline_tech_skip(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(TechTaskState.ChoiceTech)
    await callback.message.answer(i18n.TECH.CHOICE_TECH(), reply_markup=kb_tech_choice())


@router.message(TechTaskState.DeadLine)
async def deadline_tech_task(message: Message, state: FSMContext, i18n: I18nContext):
    try:
        date_time = datetime.datetime.strptime(message.text + " +0300", '%H:%M %d.%m.%y %z')
        await state.update_data(deadline=str(date_time))
    except Exception as e:
        print(f"set_deadline_tech - {e}")
        await message.answer(i18n.DEADLINE_ERROR(), reply_markup=kb_skip_deadline_tech)
        return

    await state.set_state(TechTaskState.ChoiceTech)
    await message.answer(i18n.TECH.CHOICE_TECH(), reply_markup=kb_tech_choice())


@router.callback_query(ChoiceTech.filter(), TechTaskState.ChoiceTech)
async def choice_tech(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    tech = callback.data.split(":")[1]
    await state.update_data(tech=tech)

    user = UserRepository().user(callback.from_user.id)
    data = await state.get_data()

    await callback.message.delete()

    if not (card_id := TrelloRepository().create_tech_task(data, user, i18n, )):
        await callback.answer(i18n.ERROR_CREATE_CARD(), show_alert=True)
        return

    card = TechRepository().card(card_id)

    await NotificationUsers.notify_new_tech(callback, card, i18n)
    await callback.message.answer(i18n.TASK_SEND_SUCCESS())

