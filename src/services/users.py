from src.repositories.base import BaseRepository
from src.models.users import User
from src.schemas.users import UserCreate, UserUpdate
from src.security import security


class UsersService:
    def __init__(self, db: BaseRepository[User]):
        self.db = db

    async def get_users(self, **filters):
        return await self.db.get_filtered(**filters)

    async def register_user(self, user_data: UserCreate) -> User:
        data = user_data.model_dump()
        password = data.pop("password")
        data["hashed_password"] = security.get_password_hash(password)
        return await self.db.add(data)

    async def authenticate_user(self, email: str, password: str) -> tuple[User, str] | None:
        user = await self.db.get_one(email=email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None

        token = security.create_token(data={"sub": str(user.id)})

        return user, token

    async def delete_user(self, id: str):
        await self.db.delete(id)

    async def update_user(self, id: str, data: UserUpdate) -> User | None:
        await self.db.edit(id, data.model_dump())
        return await self.db.get_by_id(id)