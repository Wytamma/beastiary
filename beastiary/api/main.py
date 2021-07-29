from os import error
from fastapi import FastAPI
from beastiary.watcher import Watcher
from fastapi import APIRouter
from beastiary.api.endpoints import runs, samples

watcher = Watcher()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/check/{path}")
async def watch(path):
    task = watcher.get(path)
    if not task:
        return {"message": "task not found"}
    if task.done():
        try:
            task.result()
            return {"message": "task ended"}
        except Exception as e:
            return {"message": str(e)}
    return {"message": "task running"}


@app.get("/watch/{path}")
async def watch(path):
    task = watcher.watch(path)
    print(watcher.tasks)
    return {"message": path}


api_router = APIRouter()
api_router.include_router(samples.router, prefix="/samples", tags=["samples"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
app.include_router(api_router)
