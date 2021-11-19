from os import error, path
from typing import Any, Optional, Callable
from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse, FileResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import URL

import logging

from beastiary.api.endpoints import traces, samples


class BeastiaryAPI(FastAPI):
    def __init__(
        self,
        title: str = "Beastiary",
        description: str = "Real-time and remote trace inspection",
        version: str = "1.2.2",
    ) -> None:
        super().__init__(
            title=title, description=description, version=version
        )  # Initialise FastAPI super class
        self.token: Optional[str] = None
        self.security: bool = True


api = BeastiaryAPI()

gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


file_path = path.abspath(path.dirname(__file__))
webapp_path = path.join(file_path, "../webapp-dist/")
index_path = path.join(file_path, "../webapp-dist/index.html")


@api.get("/")
async def index() -> FileResponse:
    return FileResponse(index_path)


@api.get("/api/security/token", tags=["security"])
async def test_token() -> Any:
    return {"token": api.token}


api_router = APIRouter(prefix="/api")
api_router.include_router(samples.router, prefix="/samples", tags=["samples"])
api_router.include_router(traces.router, prefix="/traces", tags=["traces"])
api.include_router(api_router)

api.mount("/", StaticFiles(directory=webapp_path))

# replace with https://tiangolo.medium.com/nice-a6eafd9a7bca
# probably need some switch to run it off
# auto_error: bool = False
@api.middleware("http")
async def auth_check(request: Request, call_next: Callable) -> Any:
    if "/api/" in request.url.path and request.app.security == True:
        token = request.headers.get("Authorization")
        if not token or len(token.split()) < 2:
            return JSONResponse(
                content={"detail": "Authorization header not provided!"},
                status_code=401,
            )
        else:
            token = token.split()[1]
        if token != request.app.token:
            return JSONResponse(content={"detail": "Invalid token!"}, status_code=401)
    response = await call_next(request)
    return response


@api.middleware("http")
async def add_custom_header(request: Request, call_next: Callable) -> Any:
    response = await call_next(request)
    if response.status_code == 404 and "/api/" not in request.url.path:
        return FileResponse(index_path)
    return response


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
