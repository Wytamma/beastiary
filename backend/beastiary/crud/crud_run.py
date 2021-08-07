from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from beastiary.crud.base import CRUDBase
from beastiary.models.run import Run
from beastiary.schemas.run import RunCreate, RunUpdate


class CRUDRun(CRUDBase[Run, RunCreate, RunUpdate]):
    pass


run = CRUDRun(Run)
