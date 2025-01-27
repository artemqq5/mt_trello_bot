from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from data.repository.TechRepository import TechRepository
from data.repository.TrelloRepository import TrelloRepository
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.BotTaskState import BotTaskState
from domain.use_case.NotificationUsers import NotificationUsers
from presentation.keyboards.tech.kb_order_tech import TechBotTask

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC, DEV]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC, DEV]))


@router.callback_query(TechBotTask.filter())
async def other_task_bot_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.update_data(category=i18n.TECH.BOT_TASK())
    await state.set_state(BotTaskState.Name)
    await callback.message.answer(i18n.TECH.BOT_TASK.NAME())


@router.message(BotTaskState.Name)
async def other_bot_task_name(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(name=message.text)
    await state.set_state(BotTaskState.Desc)
    await message.answer(i18n.TECH.BOT_TASK.DESC())


@router.message(BotTaskState.Desc)
async def other_bot_task_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)
    await state.set_state(None)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.OTHER_TASK.CARD_DESC(
            desc=data['desc']
        )
    )

    await state.update_data(tech='Artem')

    user = UserRepository().user(message.from_user.id)
    data = await state.get_data()

    if not (card_id := TrelloRepository().create_task_bot(data, user, i18n, )):
        await message.answer(i18n.ERROR_CREATE_CARD(), show_alert=True)
        return

    card = TechRepository().card(card_id)

    await NotificationUsers.notify_new_bot(message, card, i18n)
    await message.answer(i18n.TASK_SEND_SUCCESS())
