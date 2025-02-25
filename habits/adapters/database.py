from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class AsyncDatabase:
    def __init__(
        self,
        pg_dsn: str,
        autocommit: bool = False,
        expire_on_commit: bool = False,
    ):
        self.engine = create_async_engine(pg_dsn, echo=False)
        self.SessionLocal = sessionmaker( # type: ignore
            self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=expire_on_commit,
            autocommit=autocommit,
        )

    def session(self):
        return self.SessionLocal()
