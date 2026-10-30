from datetime import datetime, timezone
from beanie import Document
from pydantic import Field

class Chats(Document):
    type: str = Field(default="private")
    users: list[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: str | None = None
    avatar_url: str | None = None
    admin_ids: list[str]
    last_message_id: str | None = None
    last_message_sender_id: str | None = None

    class Settings:
        name = "chats"