from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from habits.core.logger import logger
from habits.errors import AlreadyExistsError, NotFoundError, ValidationError
from habits.api import endpoints
from habits.settings import settings


app = FastAPI(
    docs_url=f"/docs",
    openapi_url=f"/openapi.json",
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        msg = error["msg"]
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8")
        errors.append({"field": field, "message": msg})
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": errors},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.detail}
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    logger.info(str(exc.detail))
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc.detail)}
    )


@app.exception_handler(AlreadyExistsError)
async def already_exists_exception_handler(request: Request, exc: AlreadyExistsError):
    logger.info(str(exc.detail))
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc.detail)}
    )
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Трекер привычек",
        version="1.0.0", 
        description="API для трекера привычек",
        routes=app.routes,
    )
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if openapi_schema["paths"][path][method]["responses"].get("422"):
                openapi_schema["paths"][path][method]["responses"]["400"] = (
                    openapi_schema["paths"][path][method]["responses"]["422"]
                )
                openapi_schema["paths"][path][method]["responses"].pop("422")
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(endpoints.root)
