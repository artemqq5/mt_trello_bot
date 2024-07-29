from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject, ReplyKeyboardRemove

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

        if not current_user:
            if not UserRepository().add(tg_user.id, tg_user.username, tg_user.language_code):
                await message.answer(text=data['i18n'].REGISTER_FAIL())
                return None

            # notify admin about registration
            # await NotificationAdmin().user_activate_bot(tg_user.id, event.bot, data['i18n'])

        return await handler(event, data)


