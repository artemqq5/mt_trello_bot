from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject
from aiogram_i18n import L

from data.repository.UserRepository import UserRepository


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return

        message = event if isinstance(event, types.Message) else event.message
        tg_user = event.from_user
        current_user = UserRepository().user(tg_user.id)

        if current_user:
            if not current_user.get('username', None):
                UserRepository().update_username(tg_user.id, tg_user.username)

            if not current_user['firstname']:
                UserRepository().update_firstname(tg_user.id, tg_user.first_name)
        else:
            await message.answer(data['i18n'].ACCESS_DENIED())
            return None

        return await handler(event, data)
