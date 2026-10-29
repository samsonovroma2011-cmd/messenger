from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.models.users import User
from src.services.users import UsersService
from src.repositories.users import UsersRepository
from src.security import security


class Services:
    def __init__(self):
        self.users_repository = UsersRepository()


        self.users = UsersService(self.users_repository)


def get_services():
    return Services()


ServicesDep = Annotated[Services, Depends(get_services)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class CurrentUser:
    async def __call__(self, token: str = Depends(oauth2_scheme)) -> User:
        payload = security.decode_token(token)

        user_id: str = payload.get("sub")

        user = await UsersRepository().get_by_id(user_id)

        return user

get_current_user = CurrentUser()


CurrentUserDep = Annotated[User, Depends(get_current_user)]