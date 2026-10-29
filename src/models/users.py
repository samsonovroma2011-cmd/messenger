from typing import Annotated
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime, timezone


class User(Document):
    nick_name: str
    user_name: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"