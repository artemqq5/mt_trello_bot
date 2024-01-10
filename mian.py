import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardRemove
from aiogram.utils import executor

from _keyboard.base_keyboard import menu_keyboard
from _keyboard.creo_keyboard.creo_keyboard import design_format_keyboard
from _keyboard.my_task.my_task_keyboard import choose_tasks_keyboard
from _keyboard.tech_keyboard.tech_keyboard import tech_format_keyboard
from config.public_config import BOT_TOKEN
from constants.base import *
from constants.creo import DESIGN_FORMAT
from constants.dep import DEP_CREO_ACCESS, DEP_TECH_ACCESS, DEP_MY_TASK_ACCESS
from constants.my_task import MANAGMENT_TASK_
from constants.tech import TECH_FORMAT
from handlers.admin.add_ import add_admin_handlers
from handlers.admin.delete_ import delte_admin_handlers
from handlers.admin.get_all import get_all_admin_handlers
from handlers.admin.mailing_all import mailing_all_admin_handlers
from handlers.creo.app_ import register_app_creo_handlers
from handlers.creo.default_ import register_default_creo_handlers
from handlers.creo.other_ import register_other_creo_handlers
from handlers.creo.start_order import register_order_creo_handlers
from handlers.creo.state_creo.creo_states import StateOrderCreo
from handlers.my_task.my_task_handler import register_my_task_handler
from handlers.my_task.state_my_task.my_task_states import StateMyTaskManage
from handlers.tech.add_offer import register_add_offer_tech_handler
from handlers.tech.campaign_ import register_create_campaign_tech_handler
from handlers.tech.edit_offer import register_edit_offer_tech_handler
from handlers.tech.mt_partners import register_mt_partners_tech_handler
from handlers.tech.other_ import register_other_tech_handler
from handlers.tech.prepare_vait import register_prepare_vait_tech_handler
from handlers.tech.pwa_ import register_pwa_tech_handler
from handlers.tech.set_domain import register_domain_tech_handler
from handlers.tech.setting_cloak import register_cloak_tech_handler
from handlers.tech.share_app import register_share_app_tech_handler
from handlers.tech.state_tech.tech_states import StateTechTask
from repository.user_repository.user_repos import UserRepository
from repository.user_repository.user_usecase import get_user_model

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dispatcher = Dispatcher(bot, storage=storage)


@dispatcher.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.reset_state()

    if UserRepository().get_user(message.chat.id) is not None:
        await message.answer(MENU, reply_markup=menu_keyboard())
    else:
        await message.answer(NOT_REGISTERED_USER, reply_markup=ReplyKeyboardRemove())


@dispatcher.message_handler(lambda m: m.text == CANCEL, state='*')
async def _cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.reset_state()
        await message.answer(CANCEL_OK, reply_markup=menu_keyboard())


@dispatcher.message_handler(lambda m: m.text in (MY_TASK, CREO, TECH))
async def _menu(message: types.Message):
    user = get_user_model(UserRepository().get_user(message.chat.id))

    if message.text == MY_TASK:
        if user.dep in DEP_MY_TASK_ACCESS:
            await StateMyTaskManage.start_manage.set()
            await message.answer(MANAGMENT_TASK_, reply_markup=choose_tasks_keyboard())
        else:
            await message.answer(NOT_ACCESS)
    elif message.text == CREO:
        if user.dep in DEP_CREO_ACCESS:
            await StateOrderCreo.format_creo.set()
            await message.answer(DESIGN_FORMAT, reply_markup=design_format_keyboard())
        else:
            await message.answer(NOT_ACCESS)
    elif message.text == TECH:
        if user.dep in DEP_TECH_ACCESS:
            await StateTechTask.set_task.set()
            await message.answer(TECH_FORMAT, reply_markup=tech_format_keyboard(user.dep))
        else:
            await message.answer(NOT_ACCESS)


# register_admin_handlers
add_admin_handlers(dispatcher)
delte_admin_handlers(dispatcher)
get_all_admin_handlers(dispatcher)
mailing_all_admin_handlers(dispatcher)

# register_creo_handlers
register_order_creo_handlers(dispatcher)  # start order
register_app_creo_handlers(dispatcher)
register_default_creo_handlers(dispatcher)
register_other_creo_handlers(dispatcher)

# register_tech_handlers
register_add_offer_tech_handler(dispatcher)
register_create_campaign_tech_handler(dispatcher)
register_edit_offer_tech_handler(dispatcher)
register_mt_partners_tech_handler(dispatcher)
register_other_tech_handler(dispatcher)
register_prepare_vait_tech_handler(dispatcher)
register_pwa_tech_handler(dispatcher)
register_domain_tech_handler(dispatcher)
register_cloak_tech_handler(dispatcher)
register_share_app_tech_handler(dispatcher)

# register_my_task_handlers
register_my_task_handler(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher, skip_updates=True)
