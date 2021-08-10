from os import error
from typing import Any
from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse, FileResponse
from starlette.middleware.cors import CORSMiddleware

from beastiary.api.endpoints import runs, samples

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("beastiary/webapp-dist/index.html")


@app.get("/api/security/token", tags=["security"])
async def test_token() -> Any:
    return {"data": app.token}


api_router = APIRouter(prefix="/api")
api_router.include_router(samples.router, prefix="/samples", tags=["samples"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
app.include_router(api_router)


app.mount("/", StaticFiles(directory="beastiary/webapp-dist"))


@app.middleware("http")
async def auth_check(request: Request, call_next):
    if "/api/" in request.url.path and request.app.security == True:
        token = request.headers.get("Authorization").split()[1]
        print(token)
        if token != request.app.token:
            return JSONResponse(content={"detail": "Invalid token!"}, status_code=401)
    response = await call_next(request)
    return response


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse("beastiary/webapp-dist/index.html")
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
