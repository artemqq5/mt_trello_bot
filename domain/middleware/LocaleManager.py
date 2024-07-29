from aiogram.types import User
from aiogram_i18n.managers import BaseManager

from data.repository.UserRepository import UserRepository


class LocaleManager(BaseManager):

    async def set_locale(self, locale: str) -> str:
        pass

    async def get_locale(self, event_from_user: User) -> str:
        current_user = UserRepository().user(event_from_user.id)
        if not current_user or not current_user['lang']:
            # update client lang in database like telegram if its equals none
            UserRepository().update_lang(event_from_user.id, event_from_user.language_code)
            return event_from_user.language_code

        return current_user['lang']
