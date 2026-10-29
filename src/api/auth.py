from fastapi import APIRouter, status
from src.api.dependencies import ServicesDep, CurrentUserDep
from src.schemas.users import UserCreate, UserResponse, UserLogin, TokenResponse

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
        service: ServicesDep,
        user_data: UserCreate
) -> UserResponse:
    return await service.users.register_user(user_data)

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login_user(
        user_data: UserLogin,
        service: ServicesDep
) -> TokenResponse:
    result = await service.users.authenticate_user(user_data.email, user_data.password)

    user, token = result
    return TokenResponse(
        access_token=token,
        user=user
    )

@router.get(
    "/me",
    response_model=UserResponse
)
async def get_me(current_user: CurrentUserDep) -> UserResponse:
    return  current_user