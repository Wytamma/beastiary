from os import error
from typing import Any
from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse, FileResponse
from starlette.middleware.cors import CORSMiddleware

from beastiary.api.endpoints import runs, samples

api = FastAPI()


@api.get("/")
async def index():
    return FileResponse("beastiary/webapp-dist/index.html")


@api.get("/api/security/token", tags=["security"])
async def test_token() -> Any:
    return {"data": api.token}


api_router = APIRouter(prefix="/api")
api_router.include_router(samples.router, prefix="/samples", tags=["samples"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api.include_router(api_router)

api.mount("/", StaticFiles(directory="beastiary/webapp-dist"))


@api.middleware("http")
async def auth_check(request: Request, call_next):
    if "/api/" in request.url.path and request.app.security == True:
        token = request.headers.get("Authorization").split()[1]
        if not token:
            return JSONResponse(
                content={"detail": "Authorization header not provided!"},
                status_code=401,
            )
        else:
            token = token.split()[1]
        print(token)
        if token != request.app.token:
            return JSONResponse(content={"detail": "Invalid token!"}, status_code=401)
    response = await call_next(request)
    return response


@api.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse("beastiary/webapp-dist/index.html")
    return response


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
