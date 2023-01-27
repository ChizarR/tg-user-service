from abc import abstractstaticmethod
from typing import Dict, List

from tortoise import Tortoise

from user_api.dao import exceptions as ex
from user_api.database.models.user import User
from user_api.helpers import db_helpers as helpers
from user_api.views import UserView


class UserDAOInterface:
    @abstractstaticmethod
    @staticmethod
    async def get_by_tg_id(tg_id: int) -> User:
        raise NotImplementedError("Get is not implemented")

    @staticmethod
    @abstractstaticmethod
    async def get_list(query_params: Dict | None) -> List[User]:
        raise NotImplementedError("Get List is not implemented")

    @staticmethod
    @abstractstaticmethod
    async def create(user_view: UserView) -> User:
        raise NotImplementedError("Create is not implemented")

    @staticmethod
    @abstractstaticmethod
    async def update(user: User, fields: Dict) -> User:
        raise NotImplementedError("Update is not implemented")

    @staticmethod
    @abstractstaticmethod
    async def update_list(users: List[User], fields: Dict) -> List[User]:
        raise NotImplementedError("Update List is not implemented")

    @staticmethod
    @abstractstaticmethod
    async def delete(user_id: int) -> User:
        raise NotImplementedError("Delete is not implemented")

    @staticmethod
    @abstractstaticmethod
    async def count(query_params: Dict | None=None) -> int:
        raise NotImplementedError("Count is not implemented")


class UserDAO(UserDAOInterface):
    @staticmethod
    async def get_by_tg_id(tg_id: int) -> User:
        user = await User.get_or_none(tg_id=tg_id)

        if user is None:
            raise ex.NoSuchUserError(f"Can't find user with tg_id: {tg_id}")

        return user

    @staticmethod
    async def get_list(query_params: Dict | None=None) -> List[User]:
        if query_params is None:
            users = await User.all()
            return users

        conn = Tortoise.get_connection("default")
        q = helpers.dict_to_select_query(User.Meta.table, query_params)
        raw_data = await conn.execute_query_dict(q)
        users = helpers.generate_user_models(raw_data)
        return users

    @staticmethod
    async def create(user_view: UserView) -> User:
        current_user = await User.get_or_none(tg_id=user_view.tg_id)

        if current_user is None:
            new_user = await User.create(
                tg_id=user_view.tg_id,
                first_name=user_view.first_name,
                last_name=user_view.last_name,
                is_bot=user_view.is_bot,
            )
            return new_user

        return current_user

    @staticmethod
    async def update(user: User, fields: Dict) -> User:
        updated_user = await user.update_from_dict(fields)
        await updated_user.save()
        return updated_user

    @staticmethod
    async def update_list(users: List[User], fields: Dict) -> List[User]:
        updated_users = []

        for user in users:
            updated_user = await user.update_from_dict(fields)
            await updated_user.save()
            updated_users.append(updated_user)

        return updated_users

    @staticmethod
    async def delete(user: User) -> User:
        updated_user = await user.update_from_dict({"is_deleted": True})
        await updated_user.save()
        return updated_user

    @staticmethod
    async def count(query_params: Dict | None=None) -> int:
        if query_params is None:
            number_of_users = await User.all().count()
            return number_of_users

        conn = Tortoise.get_connection("default")
        q = helpers.dict_to_count_query(User.Meta.table, query_params)
        raw_data = await conn.execute_query_dict(q)
        res = helpers.get_count_res(raw_data)

        return res

