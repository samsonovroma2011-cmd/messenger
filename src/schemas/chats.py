from pydantic import BaseModel, Field

class ChatCreate(BaseModel):
    chat_type: str = Field(default="private")
    users: list[str]
    title: str
    description: str
    avatar_url: str | None = None


class ChatUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    avatar_url: str | None = None