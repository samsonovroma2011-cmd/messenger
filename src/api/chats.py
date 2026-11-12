from fastapi import APIRouter, status, Body
from src.api.dependencies import CurrentUserDep, ServicesDep
from src.schemas.chats import ChatCreate, ChatUpdate
from src.models.chats import Chat

router = APIRouter(prefix="/chats", tags=["Чаты"])

@router.post(
    "/",
    response_model=Chat,
    status_code=status.HTTP_201_CREATED
)
async def create_chat(
        chat_data: ChatCreate,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> Chat:
    return await service.chats.create_chat(chat_data, current_user.id)

@router.get(
    "/",
    response_model=list[Chat]
)
async def get_user_chats(current_user: CurrentUserDep, service: ServicesDep) -> list[Chat]:
    return await service.chats.get_user_chats(current_user.id)

@router.get(
    "/{chat_id}",
    response_model=Chat
)
async def get_chat_by_id(
        chat_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> Chat:
    return await service.chats.get_chat_by_id(chat_id, current_user.id)

@router.patch(
    "/{chat_id}",
    response_model=Chat
)
async def update_chat(
        chat_id: str,
        chat_data: ChatUpdate,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> Chat:
    return await service.chats.update_chat(chat_id, current_user.id, chat_data)

@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_chat(
        chat_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> None:
    return await service.chats.delete_chat(chat_id, current_user.id)

@router.post(
    "/{chat_id}/members",
    response_model=Chat
)
async def add_user_to_chat(
        chat_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep,
        new_user_id: str = Body(..., embed=True)
) -> Chat:
    return await service.chats.add_user_to_chat(chat_id, current_user.id, new_user_id)

@router.delete(
    "/{chat_id}/members/{target_user_id}",
    response_model=Chat
)
async def remove_user_from_chat(
        chat_id: str,
        target_user_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> Chat:
    return await service.chats.remove_user_from_chat(chat_id, current_user.id, target_user_id)

@router.delete(
    "/{chat_id}/leave",
    status_code=status.HTTP_204_NO_CONTENT
)
async def leave_from_chat(
        chat_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> None:
    return await service.chats.leave_from_chat(chat_id, current_user.id)

@router.post(
    "/{chat_id}/admins",
    response_model=Chat
)
async def promote_to_admin(
        chat_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep,
        target_user_id: str = Body(..., embed=True)
) -> Chat:
    return await service.chats.promote_to_admin(chat_id, current_user.id, target_user_id)

@router.delete(
    "/{chat_id}/admins/{target_user_id}",
    response_model=Chat
)
async def demote_from_admin(
        chat_id: str,
        target_user_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep
) -> Chat:
    return await service.chats.demote_from_admin(chat_id, current_user.id, target_user_id)

@router.patch(
    "/{chat_id}/owner",
    response_model=Chat,
)
async def transfer_ownership(
        chat_id: str,
        current_user: CurrentUserDep,
        service: ServicesDep,
        new_owner_id: str = Body(..., embed=True)
) -> Chat:
    return await service.chats.transfer_ownership(chat_id, current_user.id, new_owner_id)