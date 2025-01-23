from fastapi import HTTPException, status


class MainException(HTTPException):
    """Базовый класс для пользовательских исключений приложения."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Произошла ошибка."

    def __init__(self, detail: str = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class NotFoundError(MainException):
    """Исключение, вызываемое, когда ресурс не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не найдено."


class NotFoundErrorCard(MainException):
    """Исключение, вызываемое, когда ресурс не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Карта не найдена"


class AlreadyExists(MainException):
    """Исключение, вызываемое, когда ресурс уже существует."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Ресурс уже существует."


class Forbidden(MainException):
    """Исключение, вызываемое при отсутствии прав доступа."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Действие запрещено."


class CurrentStepForbidden(MainException):
    """Исключение, вызываемое при отсутствии прав доступа заполнения шага заявки."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Заполнение шага запрещено, т.к. не заполнен предыдущий."


class LeadActionForbidden(MainException):
    """Исключение, вызываемое при отсутствии прав доступа заполнения шага заявки."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = (
        "Выполнение действия запрещено, т.к. статус заявки не соответствует ожидаемому."
    )


class LeadCreationForbidden(MainException):
    """Исключение, вызываемое при наличии другой активной заявки."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Создание заявки запрещено, т.к. уже есть активная заявка."


class TokenExpiredException(MainException):
    """Исключение, вызываемое при истечении срока действия токена."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек."


class TokenAbsentException(MainException):
    """Исключение, вызываемое при отсутствии токена."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует."


class IncorrectTokenFormatException(MainException):
    """Исключение, вызываемое при неверном формате токена."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена."


class IncorrectPhoneNumberException(MainException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный формат номера телефона."


class BadRequestException(MainException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request."


class IncorrectEmailOrPasswordException(MainException):
    """Исключение, вызываемое при неверном email или пароле."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль."


class OperationsInProgressException(MainException):

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Операция в процессе выполнения."
