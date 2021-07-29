from typing import Optional

from pydantic import BaseModel


# Shared properties
class SampleBase(BaseModel):
    sample: int
    data: dict
    run_id: int


# Properties to receive on Sample creation
class SampleCreate(SampleBase):
    pass


# Properties to receive on Sample update
class SampleUpdate(SampleBase):
    pass


# Properties shared by models stored in DB
class SampleInDBBase(SampleBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Sample(SampleInDBBase):
    pass


# Properties properties stored in DB
class SampleInDB(SampleInDBBase):
    pass
