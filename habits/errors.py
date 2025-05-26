from dataclasses import dataclass


@dataclass
class BaseError(RuntimeError):
    detail: str


class NotFoundError(BaseError):
    pass


class NotFoundError(BaseError):
    pass


class ValidationError(BaseError):
    pass


class AlreadyExistsError(BaseError):
    pass

