class BaseAppError(Exception):
    pass

class AppHTTPError(BaseAppError):
    status_code: int = 500
    detail: str = "Неожиданная ошибка"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class BadRequestError(AppHTTPError):
    status_code = 400

class UnauthorizedError(AppHTTPError):
    status_code = 401

class ForbiddenError(AppHTTPError):
    status_code = 403

class NotFoundError(AppHTTPError):
    status_code = 404

class ConflictError(AppHTTPError):
    status_code = 409


class UserNotFoundError(NotFoundError):
    detail = "Пользователь не найден"

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