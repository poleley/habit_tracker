from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class base settings for application."""

    secret_key: str

    # База данных
    database_username: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    test_database_host: str
    test_database_port: int

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
            f"postgresql+asyncpg://{self.database_username}:{self.database_password}@{self.test_database_host}:"
            f"{self.test_database_port}/{self.database_name}"
        )

    class Config:
        """Special class."""

        env_file = ".env"


settings = Settings()

