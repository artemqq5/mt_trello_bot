from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.tech.OtherTaskState import OtherTaskState
from domain.state.tech.TechTaskState import TechTaskState
from presentation.keyboards.tech.kb_order_tech import TechOtherTask, kb_skip_deadline_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC, DEV]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC, DEV]))


@router.callback_query(TechOtherTask.filter())
async def other_task_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(OtherTaskState.Desc)
    await state.update_data(category=i18n.TECH.OTHER_TASK())
    await callback.message.answer(i18n.TECH.OTHER_TASK.DESC())


@router.message(OtherTaskState.Desc)
async def other_task_desc(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(desc=message.text)

    data = await state.get_data()
    await state.update_data(
        description_card=i18n.TECH.OTHER_TASK.CARD_DESC(
            desc=data['desc']
        )
    )

    await state.set_state(TechTaskState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_deadline_tech)
