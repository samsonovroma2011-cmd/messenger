from fastapi import APIRouter, Query
from src.api.dependencies import ServicesDep, CurrentUserDep
from src.schemas.users import UserResponse
from src.schemas.users import UserUpdate, UserFilter

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", response_model=list[UserResponse])
async def get_users(
        service: ServicesDep,
        filters: UserFilter = Query()
) -> list[UserResponse]:
    return await service.users.get_users(**filters.model_dump(exclude_none=True))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        service: ServicesDep,
        user_id: str
) -> UserResponse:
    return await service.users.get_by_id(user_id)

@router.patch("/me", response_model=UserResponse)
async def update_user(
        user_data: UserUpdate,
        service: ServicesDep,
        current_user: CurrentUserDep
) -> UserResponse:
    return await service.users.update_user(current_user.id, user_data)

@router.delete("/me", response_model=UserResponse)
async def delete_user(
        service: ServicesDep,
        current_user: CurrentUserDep
):
    await service.users.delete_user(current_user.id)
    return {"status_code": 200}