from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.api.dependencies import ServicesDep, CurrentUserDep
from src.schemas.users import UserCreate, UserResponse, TokenResponse

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
        service: ServicesDep,
        user_data: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
    result = await service.users.login_user(user_data.username, user_data.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user, token = result
    return TokenResponse(
        access_token=token,
        user=UserResponse(**user.model_dump())
    )

@router.get(
    "/me",
    response_model=UserResponse
)
async def get_me(current_user: CurrentUserDep) -> UserResponse:
    return  current_user