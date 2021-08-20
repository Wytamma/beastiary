from pydantic import BaseModel
from pathlib import Path
from typing import Optional


# Shared properties
class TraceBase(BaseModel):
    path: Path


# Properties to receive on Trace creation
class TraceCreate(TraceBase):
    pass


# Properties to receive on Trace update
class TraceUpdate(TraceBase):
    pass


# Properties shared by models stored in DB
class TraceInDBBase(TraceBase):
    id: int
    headers_line: str
    last_byte: int

    class Config:
        orm_mode = True


# Properties to return to client
class Trace(TraceInDBBase):
    pass


# Properties properties stored in DB
class TraceInDB(TraceInDBBase):
    pass
