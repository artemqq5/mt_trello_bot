from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from data.const import ADMIN
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from presentation.keyboards.admin.kb_users import ShowUserNav, kb_show_users, text_users_category, ShowUser, kb_user_back, \
    ShowUserBack

router = Router()

router.message.middleware(IsRoleMiddleware((ADMIN,)))
router.callback_query.middleware(IsRoleMiddleware((ADMIN,)))


@router.callback_query(ShowUserNav.filter())
async def showuser_nav(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    page = int(callback.data.split(":")[1])

    await state.update_data(showuser_nav_page=page)
    await callback.message.edit_text(text=text_users_category(page), reply_markup=kb_show_users(page))


@router.callback_query(ShowUser.filter())
async def showuser(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    id_user = callback.data.split(":")[1]
    user = UserRepository().user(id_user)

    firstname = user['firstname'] if user['firstname'] else "-"
    username = user['username'] if user['username'] else "-"
    tds_id = user['tds_buyer_id'] if user['tds_buyer_id'] else "-"

    await callback.message.edit_text(
        i18n.ADMIN.GET_USER_INFO(
            tg=user['id_user'],
            nickname=user['name_user'],
            firstname=firstname,
            username=username,
            dep=user['dep_user'],
            tds=tds_id
        ), reply_markup=kb_user_back)


@router.callback_query(ShowUserBack.filter())
async def showuser_back(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()
    page = data.get("showuser_nav_page", 1)
    await callback.message.edit_text(text=text_users_category(page), reply_markup=kb_show_users(page))
