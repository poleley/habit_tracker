import decimal
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, Optional, Union

import jwt


def normalize_phone_number(phone_number: str) -> str:
    phone_number = "".join(re.findall(r"\d", phone_number))
    if len(phone_number) < 2:
        return phone_number
    return "+7" + phone_number[1:] if phone_number[0] == "8" else "+" + phone_number


def all_nested_values_to_string(obj: datetime | dict) -> str | dict:
    if isinstance(obj, datetime) or isinstance(obj, date):
        obj = obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        obj = str(obj)
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = all_nested_values_to_string(obj[key])
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = all_nested_values_to_string(obj[i])
    return obj


@dataclass
class MockResponse:
    def __init__(
        self, expected_response_body: dict, expected_response_status: int
    ) -> None:
        self.response = expected_response_body
        self.status = expected_response_status


class JWTHandler:
    def __init__(
        self, secret_key: str, algorithm: str = "HS256", expiration_minutes: int = 30
    ):
        """
        Класс для работы с JWT токенами.

        :param secret_key: Секретный ключ для подписи токенов.
        :param algorithm: Алгоритм для подписи токенов.
        :param expiration_minutes: Время жизни токена в минутах.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def create_token(
        self, data: Dict[str, Union[str, int]], expiration_minutes: Optional[int] = None
    ) -> str:
        """
        Создает JWT токен.

        :param data: Данные, которые будут записаны в токен (payload).
        :param expiration_minutes: Время жизни токена в минутах. Если не указано, используется значение по умолчанию.
        :return: JWT токен в виде строки.
        """
        payload = data.copy()
        exp = datetime.utcnow() + timedelta(
            minutes=expiration_minutes or self.expiration_minutes
        )
        payload["exp"] = exp
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Union[str, int]]:
        """
        Декодирует JWT токен и возвращает его содержимое.

        :param token: JWT токен.
        :return: Декодированные данные токена (payload).
        :raises jwt.ExpiredSignatureError: Если срок действия токена истек.
        :raises jwt.InvalidTokenError: Если токен недействителен.
        """
        options = {"verify_signature": False}
        return jwt.decode(
            token, self.secret_key, algorithms=[self.algorithm], options=options
        )

    def is_token_valid(self, token: str) -> bool:
        """
        Проверяет, является ли токен валидным.

        :param token: JWT токен.
        :return: True, если токен валидный, иначе False.
        """
        try:
            self.decode_token(token)
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
