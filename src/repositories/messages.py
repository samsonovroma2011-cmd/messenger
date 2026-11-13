from src.repositories.base import BaseRepository
from src.models.messages import Message

class MessagesRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Message)