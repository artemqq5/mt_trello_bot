from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from data.const import ADMIN

from domain.filter.IsDepFilter import IsDepFilter
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.admin.AdminSystemState import AdminSystemState
from domain.use_case.NotificationUsers import NotificationUsers
from presentation.keyboards.kb_menu import kb_menu_all

router = Router()

router.message.middleware(IsRoleMiddleware((ADMIN,)))
router.callback_query.middleware(IsRoleMiddleware((ADMIN,)))


@router.message(AdminSystemState.MailingAll)
async def mailing_all2(message: Message, state: FSMContext, i18n: I18nContext):
    await NotificationUsers.mailing_users(message, i18n)
    await state.clear()
