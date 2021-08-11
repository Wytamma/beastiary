from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from beastiary.crud.base import CRUDBase
from beastiary.models.trace import Trace
from beastiary.schemas.trace import TraceCreate, TraceUpdate


class CRUDTrace(CRUDBase[Trace, TraceCreate, TraceUpdate]):
    pass


trace = CRUDTrace(Trace)
