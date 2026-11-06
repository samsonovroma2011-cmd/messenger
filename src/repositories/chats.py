from datetime import timezone, datetime
from schemas.chats import ChatUpdate
from src.repositories.base import BaseRepository
from src.models.chats import Chats

class ChatsRepository(BaseRepository[Chats]):
    def __init__(self):
        super().__init__(model=Chats)

    async def chat_uniqueness_check(self, users_ids: list[str]) -> bool:
        return await self.model.find_one({
            "users_ids": {"$all": users_ids, "$size": len(users_ids)}
        }) is None

    async def get_user_chats(self, current_user_id: str) -> list[Chats]:
        return await self.model.find(
            {"users_ids": current_user_id}
        ).sort("-updated_at").to_list()

    async def edit_chat(self, chat_id: str, update_data: dict) -> Chats | None:
        if any(key.startswith("$") for key in update_data.keys()):
            if "$set" not in update_data:
                update_data["$set"] = {}
            update_data["$set"]["updated_at"] = datetime.now(timezone.utc)
        else:
            update_data = {
                "$set": {
                    **update_data,
                    "updated_at": datetime.now(timezone.utc)
                }
            }

        return await self.edit(chat_id, update_data)
