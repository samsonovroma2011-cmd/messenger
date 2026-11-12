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