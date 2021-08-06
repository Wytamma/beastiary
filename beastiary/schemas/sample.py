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


# Properties to return to client
class Sample(SampleBase):
    pass
