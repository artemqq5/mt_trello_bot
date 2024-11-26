from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

router = Router()


@router.message(Command("get_id"))
async def get_id(message: Message, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await message.answer(i18n.GET_USER_ID(telegram_id=str(message.from_user.id)))
