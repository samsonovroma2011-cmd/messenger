from src.models.users import User
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(model=User)