from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from bson import ObjectId

class UserCreate(BaseModel):
    nick_name: str
    user_name: str = Field(max_length=30)
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    nick_name: str | None = None
    user_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: str
    nick_name: str
    user_name: str
    email: EmailStr
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserFilter(BaseModel):
    user_name: str | None = None
    nick_name: str | None = None
    email: EmailStr | None = None