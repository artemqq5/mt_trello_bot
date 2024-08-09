from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from data.const import MY_TASKS_ACCESS
from data.repository.CreoRepository import CreoRepository
from data.repository.TechRepository import TechRepository
from data.repository.TrelloRepository import TrelloRepository
from domain.handler.my_task import comment_task, delete_task
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from presentation.keyboards.my_task.kb_my_task import TechTaskInfo, CreoTaskInfo, MyTaskNav, kb_show_task, \
    kb_manage_task, MyTaskBack

router = Router()

router.include_routers(
    comment_task.router,
    delete_task.router
)

router.message.middleware(IsRoleMiddleware(MY_TASKS_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(MY_TASKS_ACCESS))


@router.callback_query(MyTaskNav.filter())
async def my_task_nav(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        i18n.MY_TASK.VIEW(),
        reply_markup=kb_show_task(
            tasks=TrelloRepository().get_all_cards_by_user(callback.from_user.id, i18n),
            current_page=page
        )
    )


@router.callback_query(TechTaskInfo.filter())
async def tech_task_info(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    card = TechRepository().card(callback.data.split(":")[1])

    await callback.message.edit_text(
        i18n.MY_TASK.TASK_TECH_TEMPLATE(
            id=card['id'],
            category=card['category'],
            date=card['date'],
            username=callback.from_user.username,
            desc=card['description']
        ), reply_markup=kb_manage_task(card['id_card'])
    )


@router.callback_query(CreoTaskInfo.filter())
async def creo_task_info(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    card = CreoRepository().card(callback.data.split(":")[1])

    await callback.message.edit_text(
        i18n.MY_TASK.TASK_CREO_TEMPLATE(
            id=card['id'],
            category=card['category'],
            date=card['date'],
            type=card['type'],
            platform=str(card['platform']),
            geo=card['geo'],
            lang=card['language'],
            currency=card['currency'],
            format=card['format'],
            offer=card['offer'],
            voice=card['voice'],
            source=card['source'],
            count=card['count'],
            username=callback.from_user.username,
            desc=card['description']
        ), reply_markup=kb_manage_task(card['id_card'])
    )


@router.callback_query(MyTaskBack.filter())
async def back_task_info(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.edit_text(
        i18n.MY_TASK.VIEW(),
        reply_markup=kb_show_task(tasks=TrelloRepository().get_all_cards_by_user(callback.from_user.id, i18n))
    )
