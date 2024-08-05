from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.repository.UserRepository import UserRepository


class IsDepFilter(BaseFilter):

    def __init__(self, dep):
        self.dep = dep

    async def __call__(self, message: Message):
        return UserRepository().user(message.from_user.id)['dep_user'] in self.dep
