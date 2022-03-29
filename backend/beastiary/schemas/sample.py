from typing import Optional

from pydantic import BaseModel


# Shared properties
class SampleBase(BaseModel):
    state: Optional[int] = None
    data: Optional[dict] = None


# Properties to receive on Sample creation
class SampleCreate(SampleBase):
    state: int
    data: dict


# Properties to receive on Sample update
class SampleUpdate(SampleBase):
    pass


# Properties shared by models stored in DB
class SampleInDBBase(SampleBase):
    trace_id: int


# Properties to return to client
class Sample(SampleInDBBase):
    pass
