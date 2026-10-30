from src.repositories.base import BaseRepository
from src.models.chats import Chats

class ChatsRepository(BaseRepository[Chats]):
    def __init__(self):
        super().__init__(model=Chats)