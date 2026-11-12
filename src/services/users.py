from exceptions import UserNotFoundError
from src.repositories.users import UsersRepository
from src.models.users import User
from src.schemas.users import UserCreate, UserUpdate
from src.security import security
import src.exceptions as ex


class UsersService:
    def __init__(self, users: UsersRepository):
        self.users = users

    async def get_users(self,
            user_name: str,
            nick_name: str,
            email: str
    ) -> list[User]:
        return await self.users.get_users(
            user_name=user_name,
            nick_name=nick_name,
            email=email
        )

    async def register_user(self, user_data: UserCreate) -> User:
        data = user_data.model_dump()
        password = data.pop("password")
        data["hashed_password"] = security.get_password_hash(password)
        return await self.users.add(data)

    async def login_user(self, user_name: str, password: str) -> tuple[User, str] | None:
        user = await self.users.get_one(user_name=user_name)
        if not user:
            raise ex.UserNotFoundError()
        if not security.verify_password(password, user.hashed_password):
            return None

        token = security.create_token(data={"sub": str(user.id)})

        return user, token

    async def delete_user(self, id: str):
        await self.users.delete(id)

    async def update_user(self, id: str, data: UserUpdate) -> User | None:
        await self.users.edit(id, data.model_dump())
        return await self.users.get_by_id(id)