import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

import private_config
from domain.handler.creo import order_creo
from domain.handler.my_task import my_task_manager
from domain.handler.offer import order_aff
from domain.handler.tech.start import order_tech
from domain.handler.users.admin import admin_commands
from domain.handler.users.other import afmgr, dev, gamblefb, gambleppc, gambleuac, gambleuac_gambleppc, \
    media, mt_partners
from domain.handler.users.special import special_commands
from domain.middleware.LocaleManager import LocaleManager
from domain.middleware.UserRegistrationMiddleware import UserRegistrationMiddleware

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(
    admin_commands.router,
    special_commands.router,
    afmgr.router,
    dev.router,
    gamblefb.router,
    gambleppc.router,
    gambleuac.router,
    gambleuac_gambleppc.router,
    media.router,
    mt_partners.router,
    ######################
    order_creo.router,
    order_tech.router,
    order_aff.router,
    ######################
    my_task_manager.router
)


async def main():
    logging.basicConfig(level=logging.INFO)
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=private_config.BOT_TOKEN, default=default_properties)

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


if __name__ == '__main__':
    asyncio.run(main())
