from datetime import date
from enum import Enum
from logging import Logger
from typing import List

from user_api.dao.user_dao import UserDAOInterface
from user_api.database.helpers import MailingType
from user_api.database.models.user import User
from user_api.views import UserView


class CountParams(Enum):
    total = "total"
    active = "active"
    inactive = "inactive"
    used_today = "used_today"
    with_mailing = "with_mailing"
    without_mailing = "without_mailing"


class UserService:
    def __init__(self, logger: Logger, user_dao: UserDAOInterface) -> None:
        # Data Access Object for User Model
        self.__user_dao = user_dao

        self._log = logger

    @property
    async def number_of_users(self) -> int:
        total_users = await self._count_users()
        return total_users

    @property
    async def number_of_active_users(self) -> int:
        active_users = await self._count_users(param=CountParams.active)
        return active_users

    @property
    async def number_of_inactive_users(self) -> int:
        inactive_users = await self._count_users(param=CountParams.inactive)
        return inactive_users

    @property
    async def number_of_used_today_users(self) -> int:
        used_today = await self._count_users(param=CountParams.used_today)
        return used_today

    @property
    async def number_of_users_with_mailing(self) -> int:
        users_with_mailing = await self._count_users(param=CountParams.with_mailing)
        return users_with_mailing

    @property
    async def number_of_users_without_mailing(self) -> int:
        users_without_mailing = await self._count_users(param=CountParams.without_mailing)
        return users_without_mailing

    async def _count_users(self, param: CountParams=CountParams.total) -> int:
        """Count users filtering it by CountParams"""
        res = await self.__user_dao.count()

        if param == CountParams.active:
            res = await self.__user_dao.count({"is_active": True})

        if param == CountParams.inactive:
            res = await self.__user_dao.count({"is_active": False})

        if param == CountParams.used_today:
            res = await self.__user_dao.count({"last_activity_date": date.today()})

        if param == CountParams.with_mailing:
            total = await self.__user_dao.count()
            without_mailing = await self.__user_dao.count({"mailing_type": MailingType.no_mailing})
            res = total - without_mailing

        if param == CountParams.without_mailing:
            res = await self.__user_dao.count({"mailing_type": MailingType.no_mailing})

        return res

    async def get_user(self, user_id: int) -> UserView:
        user = await self.__user_dao.get(user_id)
        view = _user_model_to_view(user)
        return view
    
    async def get_all_users(self) -> List[UserView]:
        all_users = await self.__user_dao.get_list()
        views = _users_list_to_views(all_users)
        return views

    async def get_active_users(self) -> List[UserView]:
        active_users = await self.__user_dao.get_list({"is_active": True})
        views = _users_list_to_views(active_users)
        return views

    async def get_inactive_users(self, date: date) -> List[UserView]:
        inactive_users = await self._update_inactive_users(date)
        views = _users_list_to_views(inactive_users)
        return views

    async def _update_inactive_users(self, last_activity_date: date) -> List[User]:
        active_users = await self.__user_dao.get_list({"is_active": True})
        inactive_users = []

        for user in active_users:
            if not self._is_active(user, last_activity_date):
                inactive_users.append(user)

        inactive_users = await self.__user_dao.update_list(inactive_users, {"is_active": False})
        return inactive_users

    async def _is_active(self, user: User, date: date) -> bool:
        if user.last_activity_date <= date:
            return False
        return True

    async def create_user(self, user: UserView) -> UserView:
        new_user = await self.__user_dao.create(user)
        view = _user_model_to_view(new_user)
        return view

    async def modify_user(self, user: UserView) -> UserView:
        current_user = await self.__user_dao.get(user.tg_id)
        updated_user = await self.__user_dao.update(current_user, user.dict())
        view = _user_model_to_view(updated_user)
        return view

    async def update_last_activity_date(self, user_id: int) -> UserView:
        user = await self.__user_dao.get(user_id)
        updated_user = await self.__user_dao.update(user, {
            "last_activity_date": date.today(),
            "is_active": True
        })
        view = _user_model_to_view(updated_user)
        return view

    async def update_mailing_type(self, user_tg_id: int, mailing_type: str) -> UserView:
        user = await self.__user_dao.get(user_tg_id)
        updated_user = await self.__user_dao.update(user, {"mailing_type": mailing_type})
        view = _user_model_to_view(updated_user)
        return view

    async def delete(self, user_id: int) -> UserView:
        user = await self.__user_dao.get(user_id)
        deleted_user = await self.__user_dao.delete(user)
        view = _user_model_to_view(deleted_user)
        return view


def _users_list_to_views(users: List[User]) -> List[UserView]:
    views = []
    for model in users:
        views.append(_user_model_to_view(model))

    return views


def _user_model_to_view(user: User) -> UserView:
        user_view = UserView(tg_id=user.tg_id, first_name=user.first_name,
                             last_name=user.last_name, is_bot=user.is_bot,
                             mailing_type=user.mailing_type, created_at=user.created_at,
                             last_activity_date=user.last_activity_date,
                             is_active=user.is_active, is_deleted=user.is_deleted)
        return user_view
