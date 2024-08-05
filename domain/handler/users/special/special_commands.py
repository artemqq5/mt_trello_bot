from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext
from aiogram_i18n.types import ReplyKeyboardRemove

from data.const import TECH, DESIGNER

from domain.filter.IsDepFilter import IsDepFilter
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from presentation.keyboards.kb_menu import kb_menu_all

router = Router()

router.message.middleware(IsRoleMiddleware((TECH, DESIGNER)))
router.callback_query.middleware(IsRoleMiddleware((TECH, DESIGNER)))


@router.message(Command("start"), IsDepFilter((TECH, DESIGNER)))
async def start(message: Message, state: FSMContext, i18n: I18nContext):
    await message.answer(i18n.START_SPECIAL(), reply_markup=ReplyKeyboardRemove())

