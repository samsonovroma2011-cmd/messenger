from src.exceptions.base import BadRequestError, ForbiddenError, NotFoundError, ConflictError

class UserAlreadyInChatError(ConflictError):
    detail = "Пользователь уже состоит в этом чате"

class ChatNotFoundError(NotFoundError):
    detail = "Чат не найден"

class ChatAlreadyExistsError(ConflictError):
    detail = "Диалог с этим пользователем уже существует"

class InvalidChatDataError(BadRequestError):
    detail = "Некорректные данные чата"

class PrivateChatLimitError(InvalidChatDataError):
    detail = "В личном чате должно быть ровно 2 участника"

class MissingChatTitleError(InvalidChatDataError):
    detail = "Групповой чат должен иметь название"

class CannotRemoveSelfError(InvalidChatDataError):
    detail = "Вы не можете удалить самого себя. Используйте выход из чата"

class UserNotAdminError(ForbiddenError):
    detail = "У вас нет прав администратора для этого действия"

class UserNotOwnerError(ForbiddenError):
    detail = "Вы не являетесь владельцем этого чата"

class UserNotInChatError(ForbiddenError):
    detail = "Вы не являетесь участником этого чата"

class UserIsAdminError(ForbiddenError):
    detail = "Нельзя удалить администратора чата"

class UserAlreadyAdminError(ConflictError):
    detail = "Пользователь уже является администратором"