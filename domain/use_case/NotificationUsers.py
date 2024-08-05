from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.repository.UserRepository import UserRepository


class NotificationUsers:

    @staticmethod
    async def mailing_users(message: Message, i18n: I18nContext):
        users = UserRepository().users()
        counter = 0
        block = 0
        other = 0

        for user in users:
            try:
                await message.bot.send_message(user['id_user'], message.html_text)
                counter += 1
            except TelegramForbiddenError as e:
                block += 1
                print(f"user({user}) | mailing_users: {e} ")
            except Exception as e:
                print(f"user({user}) | mailing_users: {e} ")
                other += 1

        print(f"messaging: {counter}/{len(users)}\nblock:{block}\nother:{other}")
        await message.answer(i18n.ADMIN.RESULT_NOTIFICATION(send=counter, users=len(users), block=block, other=other))

    @staticmethod
    async def notify_new_creo(callback: CallbackQuery, card: dict, i18n: I18nContext):
        users = tuple(UserRepository().designers()) + tuple(UserRepository().admins())
        counter = 0
        block = 0
        other = 0

        for user in users:
            try:
                with i18n.use_locale(user.get('lang', 'uk')):
                    await callback.bot.send_message(
                        user['id_user'],
                        i18n.CREO.NOTIFICATION_CARD(
                            id=card['id'], type=card['type'], category=card['category'], desc=card['description'],
                            username=callback.from_user.username, url=card['url']
                        )
                    )
                counter += 1
            except TelegramForbiddenError as e:
                block += 1
                print(f"user({user}) | notify_new_creo: {e} ")
            except Exception as e:
                print(f"user({user}) | notify_new_creo: {e} ")
                other += 1

        print(f"notify_new_creo: {counter}/{len(users)}\nblock:{block}\nother:{other}")
