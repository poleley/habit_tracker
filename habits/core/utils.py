import functools
import typing

from pydantic import ValidationError

from bitrix import errors
from bitrix.core.logger import logger


def handle_exceptions_in_kafka_subscriber(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    async def _wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            # Если валидация не прошла, отклоняем сообщение
            logger.error(
                f"Validation error in {func.__name__} called with args {signature}. Exception: {str(e)}"
            )
            await kwargs.get("msg").nack()
        except errors.ValidationError as e:
            logger.error(
                f"Validation error in {func.__name__} called with args {signature}. Exception: {str(e)}"
            )
        except Exception as e:
            logger.error(
                f"Exception in {func.__name__} called with args {signature}. Exception: {str(e)}"
            )

    return _wrapper
