from src.exceptions.base import NotFoundError, ConflictError

class UserNotFoundError(NotFoundError):
    detail = "Пользователь не найден"