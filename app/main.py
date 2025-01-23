from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.habit_tracker.api.endpoints.habits import router as router_habits


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Evnet on start app."""
    # Postgres
    if settings.mode == "prod":
        engine = create_async_engine(settings.database_url)
    else:
        engine = create_async_engine(settings.test_database_url, poolclass=NullPool)

    app.state.pg_async_session_maker = async_sessionmaker(
        engine, expire_on_commit=False
    )
    print("Application lifespan started.")
    yield
    print("Application lifespan finished.")


app = FastAPI(
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


for router in [router_habits]:
    app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
