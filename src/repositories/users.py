import re
from src.models.users import User
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(model=User)

    async def get_users(
            self,
            user_name: str | None = None,
            nick_name: str | None = None,
            email: str | None = None
    ) -> list[User]:
        filters = {}

        if user_name:
            filters["user_name"] = {"$regex": re.escape(user_name), "$options": "i"}
        if nick_name:
            filters["nick_name"] = {"$regex": re.escape(nick_name), "$options": "i"}
        if email:
            filters["email"] = {"$regex": re.escape(email), "$options": "i"}

        if not filters:
            return await self.model.find({}).limit(50).to_list()

        users = await self.model.find(filters).limit(50).to_list()
        return users