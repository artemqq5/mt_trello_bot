from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from data.const import ADMIN
from domain.filter.IsDepFilter import IsDepFilter
from domain.handler.creo import order_creo
from domain.handler.users.admin.command_ import delete_user, get_all, mailing_all, add_user
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.admin.AdminSystemState import AdminSystemState
from presentation.keyboards.admin.kb_users import text_users_category, kb_show_users
from presentation.keyboards.kb_menu import kb_menu_all

router = Router()

router.include_routers(
    add_user.router,
    delete_user.router,
    get_all.router,
    mailing_all.router,
)

router.message.middleware(IsRoleMiddleware((ADMIN,)))
router.callback_query.middleware(IsRoleMiddleware((ADMIN,)))


@router.message(Command("start"), IsDepFilter((ADMIN,)))
async def start(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await message.answer(i18n.START_ADMIN(), reply_markup=kb_menu_all)


@router.message(Command("add_user"))
async def add_user1(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(AdminSystemState.AddUser)
    await message.answer(i18n.ADMIN.ADD_USER())


@router.message(Command("delete_user"))
async def delete_user1(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(AdminSystemState.DeleteUser)
    await message.answer(i18n.ADMIN.DELETE_USER())


@router.message(Command("get_all"))
async def get_all(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(AdminSystemState.GetAll)
    await message.answer(text=text_users_category(), reply_markup=kb_show_users())


@router.message(Command("mailing_all"))
async def mailing_all1(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await state.set_state(AdminSystemState.MailingAll)
    await message.answer(i18n.ADMIN.INPUT_TEXT_MAILING())
