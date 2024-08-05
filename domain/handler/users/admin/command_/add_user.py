from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from data.TrelloManager import TrelloManager
from data.const import ADMIN, ALL_DEP
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.admin.AdminSystemState import AdminSystemState
from private_config import ID_BOARD_CREO, ID_BOARD_TECH

router = Router()

router.message.middleware(IsRoleMiddleware((ADMIN,)))
router.callback_query.middleware(IsRoleMiddleware((ADMIN,)))


@router.message(AdminSystemState.AddUser)
async def add_user2(message: Message, state: FSMContext, i18n: I18nContext):
    data_user = message.text.split(" ")

    if len(data_user) != 3:
        await message.answer(i18n.ADMIN.ADD_USER_ERROR_FORMAT())
        return

    if UserRepository().user(data_user[0]):
        await message.answer(i18n.ADMIN.USER_ALREADY_EXIST())
        return

    if data_user[2] not in ALL_DEP:
        await message.answer(i18n.ADMIN.ADD_USER_ERROR_DEP(dep=str(ALL_DEP)))
        return

    label_creo = TrelloManager()._create_label(data_user[1], ID_BOARD_CREO)
    label_tech = TrelloManager()._create_label(data_user[1], ID_BOARD_TECH)

    if label_creo and label_tech and not UserRepository().add(
            id_user=data_user[0], name_user=data_user[1], dep_user=data_user[2],
            label_tech=label_tech, label_creo=label_creo
    ):
        await message.answer(i18n.ADMIN.USER_ADD_FAIL())
        return

    await message.answer(i18n.ADMIN.USER_ADD_SUCCESS())
