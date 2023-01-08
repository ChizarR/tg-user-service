from logging import Logger
from typing import Dict

from fastapi.routing import APIRouter

from user_api.dao import UserDAO
from user_api.dao.exceptions import NoSuchUser
from user_api.views import UserView
from user_api.services import UserService
from user_api.helpers import rest_helpers as rest


class UserRouter:
    def __init__(self, logger: Logger) -> None:
        self._router = APIRouter(prefix="/users")
        self.register_routers()
        
        self._log = logger 
        self.__u_service = UserService(self._log, UserDAO())

    def register_routers(self) -> None:
        self._router.add_api_route("/get", self.get_all_users, methods=["GET"], status_code=200)
        self._router.add_api_route("/get/{tg_id}", self.get_user, methods=["GET"], status_code=200)
        self._router.add_api_route("/create", self.create_user, methods=["POST"], status_code=201)
        self._router.add_api_route("/update/{tg_id}", self.create_user, methods=["PUT"], status_code=200)
        self._router.add_api_route("/delete/{tg_id}", self.delete_user, methods=["DELETE"], status_code=200)

        # Test route
        self._router.add_api_route("/", self.test, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        return self._router

    async def test(self):
        return {"status": "ok"}

    async def get_all_users(self) -> Dict:
        try:
            users = await self.__u_service.get_all_users()
            r = rest.ApiResponse(status=rest.ApiResponseStatus.OK, message="All users", result=users)
            return r.to_dict()
        except Exception as e:
            self._log.error(e)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.ERROR, message=str(e))
            return r.to_dict()


    async def get_user(self, tg_id: int) -> Dict:
        try:
            user = await self.__u_service.get_user(tg_id)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.OK, message=f"User {tg_id}", result=user)
            return r.to_dict()
        except NoSuchUser as e:
            self._log.info(e)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.NO_CONTENT)
            return r.to_dict()

    async def create_user(self, user: UserView) -> Dict:
        try:
            user = await self.__u_service.create_user(user)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.OK, message="Created", result=user)
            return r.to_dict()
        except Exception as e:
            self._log.info(e)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.ERROR)
            return r.to_dict()

    async def modify_user(self, user: UserView) -> Dict:
        try:
            user = await self.__u_service.modify_user(user)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.OK, message="Modified", result=user)
            return r.to_dict()
        except Exception as e:
            self._log.info(e)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.ERROR)
            return r.to_dict()

    async def delete_user(self, tg_id: int) -> Dict:
        try:
            user = await self.__u_service.delete(tg_id)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.OK, message="Modified", result=user)
            return r.to_dict()
        except Exception as e:
            self._log.info(e)
            r = rest.ApiResponse(status=rest.ApiResponseStatus.ERROR)
            return r.to_dict()

