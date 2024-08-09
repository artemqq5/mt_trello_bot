from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from data.TrelloManager import TrelloManager
from data.const import MY_TASKS_ACCESS
from data.repository.CreoRepository import CreoRepository
from data.repository.TechRepository import TechRepository
from data.repository.TrelloRepository import TrelloRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.my_task.MyTaskState import MyTaskState
from presentation.keyboards.my_task.kb_my_task import TechTaskInfo, CreoTaskInfo, MyTaskNav, kb_show_task, \
    kb_manage_task, MyTaskBack, DeleteTask, kb_delete_back, MyTaskDeleteYES

router = Router()

router.message.middleware(IsRoleMiddleware(MY_TASKS_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(MY_TASKS_ACCESS))


@router.callback_query(DeleteTask.filter())
async def delete_task_info(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    card_id_trello = callback.data.split(":")[1]
    await state.set_state(MyTaskState.Delete)
    await state.update_data(card_id=card_id_trello)
    await callback.message.edit_text(i18n.MY_TASK.DELETE_TASK(), reply_markup=kb_delete_back)


@router.callback_query(MyTaskDeleteYES.filter(), MyTaskState.Delete)
async def access_delete(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()
    delete = TrelloManager()._delete_card(data['card_id'])

    if not delete:
        await callback.message.edit_text(i18n.MY_TASK.DELETE_FAIL(), reply_markup=kb_delete_back)
        return

    await callback.message.edit_text(
        i18n.MY_TASK.VIEW(),
        reply_markup=kb_show_task(tasks=TrelloRepository().get_all_cards_by_user(callback.from_user.id, i18n))
    )
    await callback.message.answer(i18n.MY_TASK.DELETE_SUCCESS())

