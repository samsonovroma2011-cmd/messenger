from src.repositories.chats import ChatsRepository
from src.repositories.users import UsersRepository
from src.models.chats import Chat
from src.schemas.chats import ChatCreate, ChatUpdate
import src.exceptions as ex

class ChatsService:
    def __init__(self, chats: ChatsRepository, users: UsersRepository):
        self.chats = chats
        self.users = users

    async def create_chat(self, chat_data: ChatCreate, creator_id: str) -> Chat:
        all_users_ids = list(set(chat_data.users_ids + [creator_id]))

        users = await self.users.get_users_by_ids(all_users_ids)

        if len(users) != len(all_users_ids):
            raise ex.UserNotFoundError()

        if chat_data.chat_type == "private":
            if len(all_users_ids) != 2:
                raise ex.PrivateChatLimitError()
            if not await self.chats.chat_uniqueness_check(all_users_ids):
                raise ex.ChatAlreadyExistsError()

        if chat_data.chat_type == "group":
            if not chat_data.title:
                raise ex.MissingChatTitleError()

        chat_dict = chat_data.model_dump()
        chat_dict["users_ids"] = all_users_ids
        chat_dict["owner_id"] = creator_id

        if chat_data.chat_type == "group":
            chat_dict["admin_ids"] = [creator_id]
        else:
            chat_dict["admin_ids"] = []

        return await self.chats.add(chat_dict)

    async def get_chat_by_id(self, chat_id: str, current_user_id: str) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if current_user_id not in chat.users_ids:
            raise ex.UserNotInChatError()

        return chat

    async def get_user_chats(self, current_user_id: str) -> list[Chat]:
        return await self.chats.get_user_chats(current_user_id)

    async def add_user_to_chat(self, chat_id: str, admin_id: str, new_user_id: str) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if admin_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        if new_user_id in chat.users_ids:
            raise ex.UserAlreadyInChatError()

        if chat.chat_type == "private":
            raise ex.InvalidChatDataError("Нельзя добавить пользователя в приватный чат")

        user = await self.users.get_by_id(new_user_id)
        if not user:
            raise ex.UserNotFoundError()

        updated_chat = await self.chats.edit_chat(
            chat_id,
            {"$push": {"users_ids": new_user_id}}
        )

        if not updated_chat:
            raise ex.ChatNotFoundError()

        return updated_chat

    async def remove_user_from_chat(self, chat_id: str, admin_id: str, target_user_id: str) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if admin_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        if target_user_id not in chat.users_ids:
            raise ex.UserNotInChatError()

        if target_user_id == chat.owner_id:
            raise ex.InvalidChatDataError("Нельзя удалить владельца чата")

        if target_user_id in chat.admin_ids:
            raise ex.UserIsAdminError()

        if target_user_id == admin_id:
            raise ex.InvalidChatDataError("Нельзя удалить самого себя. Используйте метод выхода")

        updated_chat = await self.chats.edit_chat( # <--- edit_chat
            chat_id,
            {"$pull": {"users_ids": target_user_id, "admin_ids": target_user_id}}
        )
        if not updated_chat:
            raise ex.ChatNotFoundError()

        return updated_chat

    async def leave_from_chat(self, chat_id: str, current_user_id: str) -> None:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if current_user_id not in chat.users_ids:
            raise ex.UserNotInChatError()

        if current_user_id == chat.owner_id:
            raise ex.InvalidChatDataError("Владелец не может выйти из чата. Сначала передайте права или удалите чат.")

        if len(chat.users_ids) == 1:
            await self.chats.delete(chat_id)
        else:
            await self.chats.edit_chat(
                chat_id,
                {
                    "$pull": {"users_ids": current_user_id, "admin_ids": current_user_id}
                }
            )

    async def update_chat(self, chat_id: str, admin_id: str, update_data: ChatUpdate) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if chat.chat_type == "private":
            raise ex.InvalidChatDataError("Нельзя изменить приватный чат")

        if admin_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        updated_chat = await self.chats.edit_chat(chat_id, update_data.model_dump(exclude_none=True))

        if not updated_chat:
            raise ex.ChatNotFoundError()

        return updated_chat

    async def delete_chat(self, chat_id: str, admin_id: str) -> None:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if admin_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        if admin_id != chat.owner_id:
            raise ex.UserNotOwnerError()

        await self.chats.delete(chat_id)

    async def promote_to_admin(self, chat_id: str, current_admin_id: str, target_user_id: str) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if current_admin_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        if target_user_id not in chat.users_ids:
            raise ex.UserNotInChatError()

        if target_user_id in chat.admin_ids:
            raise ex.UserAlreadyAdminError()

        updated_chat = await self.chats.edit_chat(
            chat_id,
            {"$push": {"admin_ids": target_user_id}}
        )
        if not updated_chat:
            raise ex.ChatNotFoundError()

        return updated_chat

    async def demote_from_admin(self, chat_id, admin_id, user_id) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if user_id not in chat.users_ids:
            raise ex.UserNotInChatError()

        if admin_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        if user_id == chat.owner_id:
            raise ex.InvalidChatDataError("Нельзя снять права с владельца чата")

        if user_id not in chat.admin_ids:
            raise ex.UserNotAdminError()

        updated_chat = await self.chats.edit_chat(
            chat_id,
            {"$pull": {"admin_ids": user_id}}
        )

        if not updated_chat:
            raise ex.ChatNotFoundError()

        return updated_chat

    async def transfer_ownership(self, chat_id: str, current_owner_id: str, new_owner_id: str) -> Chat:
        chat = await self.chats.get_by_id(chat_id)
        if not chat:
            raise ex.ChatNotFoundError()

        if chat.chat_type == "private":
            raise ex.InvalidChatDataError("Нельзя передать владельца приватного чата")

        if current_owner_id != chat.owner_id:
            raise ex.UserNotOwnerError()

        if new_owner_id not in chat.users_ids:
            raise ex.UserNotInChatError()

        if new_owner_id == current_owner_id:
            raise ex.InvalidChatDataError("Пользователь уже является владельцем")

        updated_chat = await self.chats.edit_chat(
            chat_id,
            {
                "$set": {"owner_id": new_owner_id},
                "$addToSet": {"admin_ids": new_owner_id}
            }
        )

        if not updated_chat:
            raise ex.ChatNotFoundError()

        return updated_chat


