from pydantic import BaseModel
from pathlib import Path


# Shared properties
class RunBase(BaseModel):
    path: Path


# Properties to receive on Run creation
class RunCreate(RunBase):
    pass


# Properties to receive on Run update
class RunUpdate(RunBase):
    pass


# Properties shared by models stored in DB
class RunInDBBase(RunBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Run(RunInDBBase):
    pass


# Properties properties stored in DB
class RunInDB(RunInDBBase):
    pass
