from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.TrelloManager import TrelloManager
from data.const import ADMIN, BUYERS_ROLE_LIST
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.admin.AddUserState import AddUserState
from presentation.keyboards.admin.kb_roles import kb_user_role, UserRoleCallback
from private_config import ID_BOARD_CREO, ID_BOARD_TECH

router = Router()

router.message.middleware(IsRoleMiddleware((ADMIN,)))
router.callback_query.middleware(IsRoleMiddleware((ADMIN,)))


@router.message(AddUserState.Name)
async def add_user_name(message: Message, state: FSMContext, i18n: I18nContext):
    if len(message.text) > 255:
        await message.answer(i18n.ADMIN.ADD_USER.ERROR_SYMBOLS())
        return

    await state.update_data(user_name=message.text)
    await state.set_state(AddUserState.TelegramID)
    await message.answer(i18n.ADMIN.ADD_USER.TELEGRAM_ID())


@router.message(AddUserState.TelegramID)
async def add_user_telegram_id(message: Message, state: FSMContext, i18n: I18nContext):
    if len(message.text) > 255:
        await message.answer(i18n.ADMIN.ADD_USER.ERROR_SYMBOLS())
        return

    if UserRepository().user(message.text):
        await message.answer(i18n.ADMIN.USER_ALREADY_EXIST())
        return

    await state.update_data(telegram_id=message.text)
    await state.set_state(AddUserState.Role)
    await message.answer(i18n.ADMIN.ADD_USER.ROLE(), reply_markup=kb_user_role)


@router.callback_query(UserRoleCallback.filter(), AddUserState.Role)
async def add_user_role(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    role = callback.data.split(":")[1]

    if role in BUYERS_ROLE_LIST:
        await state.update_data(user_role=role)
        await state.set_state(AddUserState.TDSBuyerID)
        await callback.message.answer(i18n.ADMIN.ADD_USER.TDS_ID())
        return

    data = await state.get_data()

    label_creo = TrelloManager()._create_label(data['user_name'], ID_BOARD_CREO)
    label_tech = TrelloManager()._create_label(data['user_name'], ID_BOARD_TECH)

    if label_creo and label_tech and not UserRepository().add(
            id_user=data['telegram_id'], name_user=data['user_name'], dep_user=role,
            label_tech=label_tech, label_creo=label_creo
    ):
        await callback.message.answer(i18n.ADMIN.ADD_USER.FAIL())
        await state.clear()
        return

    await state.clear()
    await callback.message.answer(i18n.ADMIN.ADD_USER.SUCCESS())


@router.message(AddUserState.TDSBuyerID)
async def add_user_tds_id(message: Message, state: FSMContext, i18n: I18nContext):
    if len(message.text) > 255:
        await message.answer(i18n.ADMIN.ADD_USER.ERROR_SYMBOLS())
        return

    data = await state.get_data()

    label_creo = TrelloManager()._create_label(data['user_name'], ID_BOARD_CREO)
    label_tech = TrelloManager()._create_label(data['user_name'], ID_BOARD_TECH)

    if label_creo and label_tech and not UserRepository().add_buyer(
            id_user=data['telegram_id'], name_user=data['user_name'], dep_user=data['user_role'],
            tds_id=message.text, label_tech=label_tech, label_creo=label_creo
    ):
        await message.answer(i18n.ADMIN.ADD_USER.FAIL())
        await state.clear()
        return

    await state.clear()
    await message.answer(i18n.ADMIN.ADD_USER.SUCCESS())
