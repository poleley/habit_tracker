from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class base settings for application."""

    secret_key: str

    # Контур
    mode: Literal["dev", "prod"]

    # База данных
    database_username: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    # Test database
    test_database_username: str
    test_database_password: str
    test_database_host: str
    test_database_port: int
    test_database_name: str

    # Кафка
    kafka_host: str
    kafka_port: int
    kafka_topic_write_summary: str
    kafka_topic_write_correcting: str

    kafka_topic_read_result: str
    kafka_group_read_result: str

    kafka_topic_read_error: str
    kafka_group_read_error: str

    kafka_topic_write_ivr: str
    kafka_topic_read_ivr: str
    kafka_group_read_ivr: str

    kafka_topic_write_partner: str
    kafka_topic_read_partner: str
    kafka_group_read_partner: str

    # Oktell
    oktell_url: str

    # Bitrix
    bitrix_url: str

    min_loan_amount: int = 1500000
    max_loan_amount: int = 100000000

    # Redis
    redis_host: str

    @property
    def kafka_url(self) -> str:
        """Url kafka."""
        return f"{self.kafka_host}:{self.kafka_port}"

    @property
    def database_url(self):
        """Url database."""
        return (
            f"postgresql+asyncpg://{self.database_username}:{self.database_password}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )

    @property
    def test_database_url(self):
        """Url database."""
        return (
            f"postgresql+asyncpg://{self.test_database_username}:{self.test_database_password}@{self.test_database_host}:"
            f"{self.test_database_port}/{self.test_database_name}"
        )

    class Config:
        """Special class."""

        env_file = ".env"


settings = Settings()
