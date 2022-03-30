from beastiary.log import logger
from typing import List
from beastiary.db import Database

from fastapi.encoders import jsonable_encoder

from beastiary.crud.base import CRUDBase
from beastiary.schemas.trace import TraceCreate, TraceUpdate, Trace


class CRUDTrace(CRUDBase[Trace, TraceCreate, TraceUpdate]):
    def create(  # type: ignore
        self, db: Database, *, obj_in: TraceCreate, headers_line: str, last_byte: int
    ) -> Trace:
        trace = obj_in.dict()
        trace.update(
            last_byte=last_byte,
            headers_line=headers_line,
            id=len(db.data[self.model.__name__]),
        )
        logger.debug(f"Adding Trace: {trace}")
        db.add(self.model.__name__, trace)
        return trace


trace = CRUDTrace(Trace)
