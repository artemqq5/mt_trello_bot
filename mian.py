import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

import private_config
from domain.middleware.LocaleManager import LocaleManager
from domain.middleware.UserRegistrationMiddleware import UserRegistrationMiddleware

# logging.basicConfig(level=logging.INFO)
#
# storage = MemoryStorage()
# bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
# dispatcher = Dispatcher(bot, storage=storage)
#
#
# @dispatcher.message_handler(commands=['start'], state='*')
# async def start(message: types.Message, state: FSMContext):
#     await state.reset_state()
#
#     if UserRepository().get_user(message.chat.id) is not None:
#         await message.answer(MENU, reply_markup=menu_keyboard())
#     else:
#         await message.answer(NOT_REGISTERED_USER, reply_markup=ReplyKeyboardRemove())
#
#
# @dispatcher.message_handler(lambda m: m.text == CANCEL, state='*')
# async def _cancel(message: types.Message, state: FSMContext):
#     if await state.get_state() is not None:
#         await state.reset_state()
#         await message.answer(CANCEL_OK, reply_markup=menu_keyboard())
#
#
# @dispatcher.message_handler(lambda m: m.text in (MY_TASK, CREO, TECH))
# async def _menu(message: types.Message):
#     user = get_user_model(UserRepository().get_user(message.chat.id))
#
#     if message.text == MY_TASK:
#         if user.dep in DEP_MY_TASK_ACCESS:
#             await StateMyTaskManage.start_manage.set()
#             await message.answer(MANAGMENT_TASK_, reply_markup=choose_tasks_keyboard())
#         else:
#             await message.answer(NOT_ACCESS)
#     elif message.text == CREO:
#         if user.dep in DEP_CREO_ACCESS:
#             await StateOrderCreo.format_creo.set()
#             await message.answer(DESIGN_FORMAT, reply_markup=design_format_keyboard())
#         else:
#             await message.answer(NOT_ACCESS)
#     elif message.text == TECH:
#         if user.dep in DEP_TECH_ACCESS:
#             await StateTechTask.set_task.set()
#             await message.answer(TECH_FORMAT, reply_markup=tech_format_keyboard(user.dep))
#         else:
#             await message.answer(NOT_ACCESS)
#
#
# # register_admin_handlers
# add_admin_handlers(dispatcher)
# delte_admin_handlers(dispatcher)
# get_all_admin_handlers(dispatcher)
# mailing_all_admin_handlers(dispatcher)
#
# # register_creo_handlers
# register_order_creo_handlers(dispatcher)  # start order
# register_app_creo_handlers(dispatcher)
# register_default_creo_handlers(dispatcher)
# register_other_creo_handlers(dispatcher)
#
# # register_tech_handlers
# register_add_offer_tech_handler(dispatcher)
# register_create_campaign_tech_handler(dispatcher)
# register_edit_offer_tech_handler(dispatcher)
# register_mt_partners_tech_handler(dispatcher)
# register_other_tech_handler(dispatcher)
# register_prepare_vait_tech_handler(dispatcher)
# register_pwa_tech_handler(dispatcher)
# register_domain_tech_handler(dispatcher)
# register_cloak_tech_handler(dispatcher)
# register_share_app_tech_handler(dispatcher)
# register_choice_tech_handler(dispatcher)
#
# # register_my_task_handlers
# register_my_task_handler(dispatcher)
#
# if __name__ == '__main__':
#     executor.start_polling(dispatcher=dispatcher, skip_updates=True)


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# dp.include_routers(
#     main_client.router,
#     main_admin.router,
# )


async def main():
    logging.basicConfig(level=logging.DEBUG)
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=private_config.BOT_TOKEN, default=default_properties)

    try:
        i18n_middleware = I18nMiddleware(
            core=FluentRuntimeCore(path='presentation/locales'),
            default_locale='en',
            manager=LocaleManager()
        )

        i18n_middleware.setup(dp)

        dp.message.outer_middleware(UserRegistrationMiddleware())  # register if client not registered
        dp.callback_query.outer_middleware(UserRegistrationMiddleware())  # register if client not registered

        # start bot
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        print(f"start bot: {e}")
        return


if __name__ == '__main__':
    asyncio.run(main())
