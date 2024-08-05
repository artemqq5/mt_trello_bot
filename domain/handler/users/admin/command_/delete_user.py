from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from data.const import ADMIN
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.admin.AdminSystemState import AdminSystemState

router = Router()

router.message.middleware(IsRoleMiddleware((ADMIN,)))
router.callback_query.middleware(IsRoleMiddleware((ADMIN,)))


@router.message(AdminSystemState.DeleteUser)
async def delete_user2(message: Message, state: FSMContext, i18n: I18nContext):
    if not UserRepository().user(message.text):
        await message.answer(i18n.ADMIN.USER_NO_EXIST())
        return

    if not UserRepository().delete(message.text):
        await message.answer(i18n.ADMIN.DELETE_USER_FAIL())
        return

    await message.answer(i18n.ADMIN.DELETE_USER_SUCCESS())
