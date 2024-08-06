from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import *
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from presentation.keyboards.tech.kb_order_tech import kb_choice_category_tech

router = Router()

router.message.middleware(IsRoleMiddleware([ADMIN, MT_PARTNERS]))
router.callback_query.middleware(IsRoleMiddleware([ADMIN, MT_PARTNERS]))

