from os import error
from fastapi import FastAPI
from fastapi import APIRouter, Request, Response
from beastiary.api.endpoints import runs, samples

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the BEASTIARY"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if "/api/" in request.url.path and request.app.uuid:
        uuid = request.query_params.get("uuid")
        if uuid != request.app.uuid:
            return Response(content={"detail": "Invalid UUID!"}, status_code=401)
    response = await call_next(request)
    return response


api_router = APIRouter(prefix="/api")
api_router.include_router(samples.router, prefix="/samples", tags=["samples"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
app.include_router(api_router)
