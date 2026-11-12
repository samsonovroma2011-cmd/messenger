from beanie import Document, PydanticObjectId
from pydantic import Field
from datetime import datetime, timezone

class Message(Document):
    chat_id: PydanticObjectId
    sender_id: PydanticObjectId
    text: str = Field(..., min_length=1, max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"
        indexes = [
            [("chat_id", 1), ("created_at", -1)],
        ]