from pydantic import BaseModel
from pathlib import Path


# Shared properties
class TreeBase(BaseModel):
    path: Path


# Properties to receive on Tree creation
class TreeCreate(TreeBase):
    pass


# Properties to receive on Tree update
class TreeUpdate(TreeBase):
    pass


# Properties shared by models stored in DB
class TreeInDBBase(TreeBase):
    id: int
    last_byte: int
    translation: dict


# Properties to return to client
class Tree(TreeInDBBase):
    pass


# Properties properties stored in DB
class TreeInDB(TreeInDBBase):
    pass
