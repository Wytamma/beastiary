from os import error
from fastapi import FastAPI
from fastapi import APIRouter, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from beastiary.api.endpoints import runs, samples

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("beastiary/webapp-dist/index.html")


api_router = APIRouter(prefix="/api")
api_router.include_router(samples.router, prefix="/samples", tags=["samples"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
app.include_router(api_router)


app.mount("/", StaticFiles(directory="beastiary/webapp-dist"))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if "/api/" in request.url.path and request.app.uuid:
        uuid = request.query_params.get("uuid")
        if uuid != request.app.uuid:
            return Response(content={"detail": "Invalid UUID!"}, status_code=401)
    response = await call_next(request)
    return response


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse("beastiary/webapp-dist/index.html")
    return response
