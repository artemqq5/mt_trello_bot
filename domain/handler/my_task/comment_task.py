from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from data.TrelloManager import TrelloManager
from data.const import MY_TASKS_ACCESS
from data.repository.TrelloRepository import TrelloRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.my_task.MyTaskState import MyTaskState
from presentation.keyboards.my_task.kb_my_task import kb_show_task, \
    CommentTask, kb_comment_back

router = Router()

router.message.middleware(IsRoleMiddleware(MY_TASKS_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(MY_TASKS_ACCESS))


@router.callback_query(CommentTask.filter())
async def comment_task_info(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    card_id_trello = callback.data.split(":")[1]
    await state.set_state(MyTaskState.Comment)
    await state.update_data(card_id=card_id_trello)
    await callback.message.edit_text(i18n.MY_TASK.COMMENT_TASK_INPUT(), reply_markup=kb_comment_back)


@router.message(MyTaskState.Comment)
async def your_comment(message: Message, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()
    comment = TrelloManager()._write_comment(data['card_id'], message.text)

    if not comment:
        await message.edit_text(i18n.MY_TASK.COMMENT_FAIL(), reply_markup=kb_comment_back)
        return

    await message.answer(
        i18n.MY_TASK.VIEW(),
        reply_markup=kb_show_task(tasks=TrelloRepository().get_all_cards_by_user(message.from_user.id, i18n))
    )
    await message.answer(i18n.MY_TASK.COMMENT_SUCCESS())
