from typing import Optional

from pydantic import BaseModel


# Shared properties
class SampleBase(BaseModel):
    state: Optional[int] = None
    newick: Optional[str] = None


# Properties to receive on Sample creation
class SampleCreate(SampleBase):
    state: int
    newick: str


# Properties to receive on Sample update
class SampleUpdate(SampleBase):
    pass


# Properties shared by models stored in DB
class SampleInDBBase(SampleBase):
    tree_id: int


# Properties to return to client
class TreeSample(SampleInDBBase):
    pass
